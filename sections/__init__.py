__author__ = 'faebser'

from section_option import Section, Option
from section_manager import register_section
import config

audio = Section()
audio.template = 'audio.html'
audio.options = dict({
    'device': Option(config.audio.device),
    'sampleRate': Option(config.audio.sampleRate, (11025, 22050, 44100)),
    'bitsPerSample': Option(config.audio.bitsPerSample, (8, 16, 32)),
    'channel': Option(config.audio.channel, (1, 2))
})

register_section('audio', audio)

general = Section()

general.template = 'general.html'

general.options = dict({
    'duration': Option(config.general.duration),
    'bufferSecs': Option(config.general.bufferSecs),
    'reconnect': Option(config.general.reconnect, ('yes', 'no')),
    'realtime': Option(config.general.realtime, ('yes', 'no'))
})

register_section('general', general)

for index, server in enumerate(config.icecast):
    tempSection = Section()
    tempSection.template = 'server.html'
    tempSection.options = dict({
        'bitrateMode': Option(server.bitrateMode, ('cbr', 'avr')),
        'format': Option(server.format, ('mp3')),
        'bitrate': Option(server.bitrate, (96, 128, 192, 320)),
        'quality': Option(server.quality),
        'server': Option(server.server),
        'password': Option(server.password),
        'mountPoint': Option(server.mountPoint),
        'name': Option(server.name),
        'description': Option(server.description),
        'url': Option(server.url),
        'gerne': Option(server.genre),
        'public': Option(server.public, ('yes', 'no')),
        'localDumpFile': Option(server.localDumpFile),
        'fileAddDate': Option(server.fileAddDate)
    })
    tempSection.index = index
    register_section(server.section_name, tempSection)