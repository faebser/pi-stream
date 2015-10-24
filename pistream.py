# -*- coding: utf-8 -*-
from bottle import run, template, static_file, get, post, request, HTTPError, debug, TEMPLATE_PATH, response, abort, delete
from display import display
from os import linesep
import subprocess
import time
import json
import config
from os import path, listdir, remove
from configparser import NoOptionError, NoSectionError, ConfigParser
#import sections
from startup_tests.test_manager import run_all_tests, TestStatus
import codecs
import select
from threading import Thread
from Queue import Queue, Empty
import re
import socket
import fcntl
import struct
from time import sleep


__author__ = 'faebser'


# Static Routes
@get('/<filename:re:.*\.js>')
def javascript(filename):
    return static_file(filename, root='js')


@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/<filename:re:.*\.(eot|ttf|woff|svg|woff2)>')
def fonts(filename):
    return static_file(filename, root='fonts')


@get('/<filename:re:.*\.(jpg|png|gif)>')
def images(filename):
    return static_file(filename, root='img')


@get('/download/<filename:re:.*\.(mp3)>')
def download_recording(filename):
    return static_file(filename, root=app_config['recording_folder'], download=True)

# globals

status = list()
app_config = dict()
darkice_config = dict()
json_content_type = 'application/json'
darkice = None
darkice_stdout_queue = Queue()
darkice_stderr_queue = Queue()
lcd_display = display.LcdDisplay()


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def init():
    global status, app_config, darkice_config

    lcd_display.info("...............\n...............")
    lcd_display.info("server\nstarting up")
    status = []

    lcd_display.info("loading\nconfig file")
    app_config_file = open(path.join('config', 'pi_stream.ini'))
    app_config.clear()
    app_config, app_config_parser_errors = parse_app_config(app_config_file)
    app_config_file.close()

    if len(app_config_parser_errors) != 0:
        status.append(app_config_parser_errors)

    if len(app_config) != 0:  # no errors
        lcd_display.info("loading default/\ndarkice config")
        darkice_config_file = open(app_config['defaultConfig'])
        darkice_config, darkice_config_parser_errors = config.init_config(darkice_config_file)
        darkice_config_file.close()

        if len(darkice_config_parser_errors) != 0:
            status.append(darkice_config_parser_errors)

    lcd_display.info("running\nstatus tests")
    status = run_all_tests()
    lcd_display.start_process()
    try:
        ip_address = get_ip_address('eth0')
        lcd_display.put(u"Reach me at\n{}".format(ip_address), lcd_display.GOOD)
    except Exception, e:
        pass # dont do anything, there will be an error in the queue anyway
    for item in status:
        if item['result'] is TestStatus.Error:
            lcd_display.put(item['lcd_message'], lcd_display.ERROR)
        if item['result'] is TestStatus.Attention:
            lcd_display.put(item['lcd_message'], lcd_display.INFO)
        pass


def parse_app_config(config_file):
    parser = ConfigParser()
    parser.read_file(config_file)
    try:
        return parser['pistream'], []
    except KeyError:
        print u"Section {0} not found in pi_stream.ini file. Please check the file".format(u'pistream')
        return {}, [(TestStatus.Error, u"Section {0} not found in pi_stream.ini file. Please check the file".format(u'pistream'))]


@get('/run-tests')
def run_all_tests_http():
    global status
    status = run_all_tests()
    return get_status()


@get('/status')
def get_status():
    global status
    json_list = [{'message': item['message'], 'status': item['result'].name.lower()} for item in status]
    response.content_type = json_content_type
    return json.dumps(json_list)


def read_nonblocking_output(stdout, stdout_queue):
    for line in iter(stdout.readline, b''):
        stdout_queue.put(line)
    stdout.close()


def read_nonblocking_error(stderr, stderr_queue):
    for line in iter(stderr.readline, b''):
        stderr_queue.put(line)
    stderr.close()


@post('/stream')
def start_stream():
    global darkice
    global darkice_stderr_queue
    global darkice_stdout_queue
    values = request.json

    alsacap = subprocess.Popen('alsacap -R', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = alsacap.communicate()

    found_usb = False
    channels = None
    sampling_rate = None
    for line in output.splitlines():
        print line
        if found_usb and 'channel' in line and 'sampling rate' in line:
            print "line:"
            print line.strip()
            channels, sampling_rate = parse_card_info_string(line.strip())
            break
        if 'USB' in line:    # start capturing data
            print "start capturing data"
            found_usb = True

    print(channels)
    print(sampling_rate)

    if channels and sampling_rate:
        darkice_config['audio'].channel.value = max(channels)  # todo fix this max/min
        darkice_config['audio'].sampleRate.value = max(sampling_rate)  # todo fix this max/min

    darkice_config['servers'][0].name.value = unicode(values['name'])
    darkice_config['servers'][0].genre.value = unicode(values['genre'])
    darkice_config['servers'][0].url.value = unicode(values['url'])
    darkice_config['servers'][0].description.value = unicode(values['description'])

    print app_config['recording_folder']
    print unicode(values['name'])

    darkice_config['servers'][0].localDumpFile.value = path.join(app_config['recording_folder'], unicode(values['name'] + '.mp3'))

    try:
        with codecs.open('test.cfg', mode='wb', encoding='utf-8') as config_file:
            config.write_to_file(config_file, darkice_config['general'], darkice_config['audio'], darkice_config['servers'])
            filename = config_file.name
            print filename
    except IOError as e:
        print("there is an error")
        return {'error': 'File not availabe: {}'.format(e)}

    darkice = subprocess.Popen('sudo darkice -c {}'.format(filename), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    # non blocking reading of stdout and stderr for darkice status
    thread_output = Thread(target=read_nonblocking_output, args=(darkice.stdout, darkice_stdout_queue))
    thread_output.daemon = True
    thread_output.start()
    thread_error = Thread(target=read_nonblocking_error, args=(darkice.stderr, darkice_stderr_queue))
    thread_error.daemon = True
    thread_error.start()

    return get_stream_status()


def parse_card_info_string(info_string):
    channels, sampling_rate = info_string.split(',')
    test = re.compile(ur'(\d+)')
    sampling_rate = re.findall(test, sampling_rate)
    channels = re.findall(test, channels)

    return channels, sampling_rate


@get('/stream')
def get_stream_status():
    global darkice_stderr_queue
    global darkice_stdout_queue

    lines = ''
    try:
        while not darkice_stdout_queue.empty():
            lines += darkice_stdout_queue.get_nowait()
    except Empty:
        print('no output yet')
    else:
        print lines

    errors = ''
    try:
        while not darkice_stderr_queue.empty():
            errors += darkice_stderr_queue.get_nowait()
    except Empty:
        print('no error yet')
    else:
        print errors

    errors_from_lines = filter(None, [parse_lines_for_error(line) for line in lines.split(linesep)])
    error_messages = filter(None, [parse_errors(error) for error in errors.split(linesep)])
    error_messages.extend(errors_from_lines)

    if len(error_messages) == 0 and darkice is not None:
        # no errors
        lcd_display.reset()
        lcd_display.clear()
        lcd_display.message('I am streaming')
        return {'link': '<a href="http://panel9.serverhostingcenter.com:2199/tunein/yfgmkhow-stream.pls">Link to the stream</a>', 'errors': len(error_messages), 'messages': error_messages}
    else:
        abort(500)


def parse_lines_for_error(line):
    if 'DarkIce:' in line and 'cpp' in line:
        return {
            'message': line,
            'status': TestStatus.Error.name.lower()
        }


def parse_errors(error):
    if len(error) != 0:
        return {
            'message': error,
            'status': TestStatus.Error.name.lower()
        }


@get('/files')
def return_files():
    global app_config
    files = listdir(app_config['recording_folder'])
    print files
    # get all files from path
    # send id, name
    return json.dumps(files)


@delete('/download/<filename:re:.*\.(mp3)>')
def delete_file(filename):
    path_to_delete = path.join(path.abspath('.'), app_config['recording_folder'], filename)
    try:
        remove(path_to_delete)
    except Exception, e:
        pass
    return


@get('/')
def index():
    # just deliver the payload
    return template('template.html')


# @get('/sections')
def get_all_section():
    """
    Return all the sections to the client

    :return: a list of all sections
    """
    return get_dicts()


# @get('/<section>')
def get_section(section):
    """
    Get the content of a section

    :param Section section:
    :return:
    """
    if section in sections:
        return sections[section].to_dict()
    else:
        raise HTTPError(500, json.dumps({'error': u'section ' + str(section) + u' is not available'}))


# @post('/<section>/<option>')
def update(section, option):
    """
    Updates a option inside a section

    :param Section section: name of section
    :param string option: name of option
    :return: error or nothing
    """
    if section in sections and option in section.options:
            value = request.params.value or None
            if value is None:
                raise HTTPError(500, json.dumps({'error': "No value provided"}))
            else:
                section.options[option] = value
                return json.dumps(section.options[option])
    else:
        raise HTTPError(500, json.dumps({'error': u'section ' + str(section) + u" or option " + str(option) + " not available"}))


# @get('/<section>/<option>')
def get(section, option):
    """
    Returns the value of a option inside a section

    :param Section section: name of section
    :param string option: name of option
    :return: value of option
    """
    if section in sections and option in sections[section].options:
        return {option: sections[section].options[option].value}
    else:
        raise HTTPError(500, json.dumps({'error': u'section ' + str(section) + u" or option " + str(option) + " not available"}))

TEMPLATE_PATH.append('./sections/templates')
init()
run(host='0.0.0.0', port=8080, debug=True)
