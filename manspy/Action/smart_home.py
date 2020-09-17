# -*- coding: utf-8 -*-

#Включи настольный свет в спальне.
#Запрос отсутствующего аргумента:
#-Включи свет в спальне. -Какой именно свет? -Настольный.

import socket
from urllib import request


FAKE_DATA = {
    'light': {
        'bedroom': {
            0: 0
        }
    }
}


def fake_smarthome(group, room, device, cond):
    FAKE_DATA[group][room][device] = cond


def smarthome(group, room, device, cond):
    url = "http://192.168.0.101/manage.php?to=" +group+ "%20" +room+ "%20" +device+ "&command=" +cond+ "&string=on"
    request.urlopen(url).read()


def LightOn(arg0, room, device):
    if arg0['answer_type'] == 'construct':
        return "0" if arg0['antonym'] else "1"
    elif arg0['answer_type'] == 'fake':
        cond = "0" if arg0['antonym'] else "1"
        return fake_smarthome('light', room, device, cond)
    if arg0['answer_type'] == 'real':
        cond = "0%200%200" if arg0['antonym'] else "1%201%201"
        return smarthome('light', room, device, cond)


def showAddress(arg0, device):
    FAKE = {'computer': '192.168.0.1'}

    if arg0['antonym']:
        return

    if device == 'computer':
        if arg0['answer_type'] == 'real':
            return str(socket.gethostbyname(socket.getfqdn()))
        elif arg0['answer_type'] in ('fake', 'construct'):
            return FAKE[device]


def printToIF(arg0, *conditions):
    for condition in conditions:
        arg0['to_IF'](condition)

''' Состояние числительных '''
def get(arg0, a): return a

def _is_only_numbers(numbers):
    for i in numbers:
        if not isinstance(i, (int, float, complex)):
            return False
    return True

def add(arg0, *a):
    ''' Сложение '''
    a = list(a)

    if not a: return 0

    if _is_only_numbers(a):

        start = a.pop(0)
        if arg0['antonym']:
            a = [-i for i in a]
        return sum(a, start)
    
    else:

        for index, i in enumerate(a): a[index] = str(a[index])
        if arg0['antonym']: return ' - '.join(a)
        return ' + '.join(a)

def multiply(arg0, *a):
    ''' Умножение '''
    a = list(a)

    if not a: return 0

    if _is_only_numbers(a):

        res = float(a.pop(0))
        if arg0['antonym']:
            for i in a: res /= i
        else:
            for i in a: res *= i
        return res

    else:

        for index, i in enumerate(a): a[index] = str(a[index])
        if arg0['antonym']: return ' / '.join(a)
        return ' * '.join(a)