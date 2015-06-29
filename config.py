__author__ = 'faebser'

import configparser
from configparser import NoOptionError, NoSectionError, ConfigParser
import tempfile
from startup_tests.test_manager import TestStatus
import json
import subprocess


class General(object):
        parser = None
        section_name = "general"

        def __init__(self, config_parser):
            self.parser = config_parser

        @property
        def duration(self):
            return self.parser.get(self.section_name, 'duration')[self.section_name]['duration']

        @duration.setter
        def duration(self, new_duration):
            self.parser.set(self.section_name, 'duration', new_duration)

        @property
        def bufferSecs(self):
            return self.parser.get(self.section_name, 'bufferSecs')

        @bufferSecs.setter
        def bufferSecs(self, new_value):
            self.parser.set(self.section_name, 'bufferSecs', new_value)

        @property
        def reconnect(self):
            return self.parser.get(self.section_name, 'reconnect')

        @reconnect.setter
        def reconnect(self, new_value):
            self.parser.set(self.section_name, 'reconnect', new_value)

        @property
        def realtime(self):
            return self.parser.get(self.section_name, 'realtime')

        @realtime.setter
        def realtime(self, new_value):
            return self.parser.set(self.section_name, 'realtime', new_value)

        #duration = Entry('duration')
        #bufferSecs = Entry('bufferSecs')
        #reconnect = Entry('reconnect')
        #realtime = Entry('realtime')


class DarkiceConfigWrapper(object):
    parser = ConfigParser()
    parser.optionxform = str
    config_file = None
    general = None

    def __init__(self, config_file):
        self.config_file = config_file
        self.parser.read_file(self.config_file)
        self.general = General(self.parser)



'''
This files parses the config file.
There is a subclass for each section in the config
'''

def section_to_dict(_section):
    obj = dict()
    for prop in _section.property_tuple:
        obj.update({
            prop.name: prop.value
        })
    return dict({_section.section_name: obj})


class Entry(object):
    value = None
    name = None

    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def setvalue(self, value):
        self.value = value

    def getvalue(self, parent):
        return self.value

    def delvalue(self):
        del self.value

    def __unicode__(self):
        return self.name + u" : " + unicode(self.value)

    def __str__(self):
        return self.__unicode__()


class General(object):
    duration = Entry('duration')
    bufferSecs = Entry('bufferSecs')
    reconnect = Entry('reconnect')
    realtime = Entry('realtime')

    section_name = 'general'

    property_tuple = (duration, bufferSecs, reconnect, realtime)

    """
    duration = property(_duration.getvalue, _duration.setvalue, _duration.delvalue, u'duration of encoding, in seconds. 0 means forever')
    bufferSecs = property(_bufferSecs.getvalue, _bufferSecs.setvalue, _bufferSecs.delvalue, u'size of internal slip buffer, in seconds. recommended is around 10-15s')
    reconnect = property(_reconnect.getvalue, _reconnect.setvalue, _reconnect.delvalue, u'reconnect to the server(s) if disconnected')
    realtime = property(_realtime.getvalue, _realtime.setvalue, _realtime.delvalue, u'No coomment provided')
    """

    def __init__(self, _section):
        for prop in self.property_tuple:
            try:
                prop.value = _section.get(prop.name)
            except NoOptionError as e:
                print 'Option {} not found in section {}'.format(e.option, e.section)


class Input(object):
    device = Entry('device')
    sampleRate = Entry('sampleRate')
    bitsPerSample = Entry('bitsPerSample')
    channel = Entry('channel')

    section_name = 'input'

    property_tuple = (device, sampleRate, bitsPerSample, channel)

    """
    device = property(_device.getvalue, _device.setvalue, _device.delvalue, u'OSS DSP soundcard device for the audio input')
    sampleRate = property(_sampleRate.getvalue, _sampleRate.setvalue, _sampleRate.delvalue, u'sample rate in Hz. try 11025, 22050 or 44100')
    bitsPerSample = property(_bitsPerSample.getvalue, _bitsPerSample.setvalue, _bitsPerSample.delvalue, u'bits per sample. try 16')
    channel = property(_channel.getvalue, _channel.setvalue, _channel.delvalue, u'channels. 1 = mono, 2 = stereo')
    """

    def __init__(self, _section):
        for prop in self.property_tuple:
            try:
                prop.value = _section.get(prop.name)
            except NoOptionError as e:
                print "Option {0} not found in section {1}".format(e.option, e.section)


class Icecast2(object):
    bitrateMode = Entry('bitrateMode')  # average bit rate
    format = Entry('format')    # format of the stream: ogg vorbis
    bitrate = Entry('bitrate')        # bitrate of the stream sent to the server
    quality = Entry('quality')
    server = Entry('server')  # host name of the server
    port = Entry('port')       # port of the IceCast2 server, usually 8000
    password = Entry('password')    # source password to the IceCast2 server
    mountPoint = Entry('mountPoint')  # mount point of this stream on the IceCast2 server
    name = Entry('name')  # name of the stream
    description = Entry('description')              # description of the stream
    url = Entry('url')               # URL related to the stream
    genre = Entry('genre')    # genre of the stream
    public = Entry('public')       # advertise this stream?
    localDumpFile = Entry('localDumpFile')  # local dump file
    fileAddDate = Entry('fileAddDate')

    property_tuple = (bitrateMode, format, bitrate, quality, server, port, password, mountPoint, name, description, url, genre, public, localDumpFile, fileAddDate)

    section_name = 'icecast2-'

    def __init__(self, _section):
        for prop in self.property_tuple:
            try:
                prop.value = _section.get(prop.name)
            except NoOptionError as e:
                print "Option {0} not found in section {1}".format(e.option, e.section)


def add_value_from_prop(_parser, prop, section_name):
    try:
        _parser.set(section_name, prop.name, unicode(prop.value))
    except NoSectionError as e:
        print "section {} not found, adding it".format(e.section)
        _parser.add_section(section_name)
        _parser.set(section_name, prop.name, unicode(prop.value))


"""
def write_to_temp_file():
    fp = tempfile.TemporaryFile()
    tempParser = configparser.ConfigParser()
    tempParser.read_file(fp)
    for prop in general.property_tuple:
        add_value_from_prop(tempParser, prop, general.section_name)
    for prop in audio.property_tuple:
        add_value_from_prop(tempParser, prop, audio.section_name)
    for index, server in enumerate(icecast):
        for prop in server.property_tuple:
            add_value_from_prop(tempParser, prop, server.section_name + str(index))
    return fp
"""


def write_to_file(fp, general_section, input_section, servers):
    temp_parser = configparser.ConfigParser()
    temp_parser.optionxform = str
    for prop in general_section.property_tuple:
        add_value_from_prop(temp_parser, prop, general_section.section_name)
    for prop in input_section.property_tuple:
        add_value_from_prop(temp_parser, prop, input_section.section_name)
    for index, server in enumerate(servers):
        for prop in server.property_tuple:
            add_value_from_prop(temp_parser, prop, server.section_name)
    temp_parser.write(fp)
    return fp


def init_config(config_file):
    parser = configparser.ConfigParser()
    icecast = list()
    general = None
    audio = None  # renamed to audio instead of input as it would shadow builtin input
    errors = []

    parser.read_file(config_file)

    try:
        general = General(parser['general'])
        audio = Input(parser['input'])
    except KeyError as error:
        print "Section {0} not found. This sections contains info needed for darkice. please check your config-file".format(error)
        errors.append((TestStatus.Error,
                      "Section {0} not found. This sections contains info need for darkice. please check your config-file".format(error)))

    for i in range(0, 7):
        try:
            name = 'icecast2-' + str(i)
            tempServer = Icecast2(parser[name])
            tempServer.section_name = name
            icecast.append(tempServer)
        except KeyError as error:
            if len(icecast) == 0:
                print "Section {0} not found. At least one server section is needed. Please add a server to your config file".format(error)
                errors.append((TestStatus.Error,
                           "Section {0} not found. At least one server section is needed. Please add a server to your config file".format(error)))

    return {"audio": audio, "general": general, "servers": icecast}, errors
