# -*- coding: utf-8 -*-
__author__ = 'faebser'

from bottle import route, run, template, view, static_file, get, post, request
import os
import subprocess
import time


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


# Static Routes
@get('/<filename:re:.*\.js>')
def javascript(filename):
    return static_file(filename, root='js')


@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='fonts')


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
run(host='0.0.0.0', port=8080, reloader=False)
