# -*- coding: utf-8 -*-
__author__ = 'faebser'

from bottle import route, run, template, view, static_file, get, post, request, HTTPError, debug, TEMPLATE_PATH, response
import os
import subprocess
import time
import json
import config
from config import section_to_dict as to_json
from sections.section_manager import get_dicts
import sections
from sections.section_manager import manager as sections
from sections.section_manager import get_all_sections
from startup_tests.test_manager import add_test, run_all_tests
import codecs
import select
from threading import Thread
from Queue import Queue, Empty


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

"""
def buildCommandString(master, targets):
    target = 'of=/dev/%s ' * len(targets)
    print(target % tuple(targets))
    command = "sudo dcfldd bs=4M if=/dev/" + master + " " + target % tuple(targets) + "sizeprobe=if statusinterval=1 2>&1 | tee progress.info"
    print(command)
    return command

@post('/clone')
def clone():
    subprocess.Popen('cat /dev/null > progress.info', shell=True)
    master = request.params.master
    targets = request.params.getall('targets[]')
    with open("progress.info", 'w+') as f:
        subprocess.Popen(buildCommandString(master, targets), stdout=f, shell=True)
    time.sleep(1)
    return progress()


@get('/progress')
def progress():
    status = subprocess.Popen('tail -n 1 progress.info', shell=True, stdout=subprocess.PIPE)
    output, error = status.communicate()
    if len(output) == 0:
        return {'progress': 0}
    if "records out" in output:
        subprocess.Popen('cat /dev/null > progress.info', shell=True)
        return {'progress': 'finish'}
    return {'progress': output.splitlines()[-1]}


@route('/')
@view('index.html')
def index():
    context = {}
    # see http://unix.stackexchange.com/questions/60299/how-to-determine-which-sd-is-usb
    usbDevices = subprocess.Popen('bash usb.sh', stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    output, errors = usbDevices.communicate()
    if len(output) == 0:  # no devices
        context.update({
            'noDevices': True
        })
        return dict(context=context)
    else:  # we have devices
        devices = []
        for device in output.splitlines():
            name, info = device.split(b';')
            devices.append({'name': name, 'info': info})
        context.update({
            'devices': devices,
            'noDevices': False
        })
        return dict(context=context)
"""

# testing
# real stuff down here
# by now the config and all the sections should be imported


# global

status = dict()
json_content_type = 'application/json'
darkice = None
darkice_stdout_queue = Queue()
darkice_stderr_queue = Queue()


def init():
    global status
    status.clear()
    status = run_all_tests()


@get('/run-tests')
def run_all_tests_http():
    global status
    status.clear()
    status = run_all_tests()
    return get_status()


@get('/status')
def get_status():
    global status
    json_list = [{'message': message, 'status': result.name.lower()} for result, message in status.iteritems()]
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

    config.icecast[0].name.value = unicode(values['name']['value'])
    config.icecast[0].genre.value = unicode(values['genre']['value'])
    config.icecast[0].url.value = unicode(values['url']['value'])
    config.icecast[0].description.value = unicode(values['description']['value'])

    with codecs.open('test.cfg', mode='wb', encoding='utf-8') as config_file:
        config.write_to_file(config_file)
        filename = config_file.name
    print filename
    darkice = subprocess.Popen('sudo darkice -c {}'.format(filename), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    # non blocking reading of stdout and stderr for darkice status
    thread_output = Thread(target=read_nonblocking_output, args=(darkice.stdout, darkice_stdout_queue))
    thread_output.daemon = True
    thread_output.start()
    thread_error = Thread(target=read_nonblocking_error, args=(darkice.stderr, darkice_stderr_queue))
    thread_error.daemon = True
    thread_error.start()

    return get_stream_status()


@get('/stream')
def get_stream_status():
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
    return {'link': 'http://panel9.serverhostingcenter.com:2199/tunein/yfgmkhow-stream.pls', 'errors': len(errors)}


@get('/')
def index():
    # render all the templates
    content = u''  # content from templates
    server_index = 0
    for name, section in sections.iteritems():
        content += template(section.template, context=section)
    return template('template.html', context=content)


@get('/sections')
def get_all_section():
    """
    Return all the sections to the client

    :return: a list of all sections
    """
    return get_dicts()


@get('/<section>')
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


@post('/<section>/<option>')
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


@get('/<section>/<option>')
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
debug(True)
init()
run(host='0.0.0.0', port=8080, reloader=True)
