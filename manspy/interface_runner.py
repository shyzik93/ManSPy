# -*- coding: utf-8 -*-
""" Модуль параллельно запускает все МИ.
    Цикл приёма сообщения от ИСУ необходимо реализовывать внутри МИ.
    Запрещено называть МИ следующими именами: all, general.

    Модуль запускаются через потоки, поэтому при зависании одного модуля встанет вся программа, например при вызове input().
    Чтобы устранить эту проблему, нужно запускать каждый МИ как отдельный процесс (прграмму), но появляется задача: как передать объект класса API/
"""
#import repper, conftools
import os
import sys
import threading
import json

_path = os.path.dirname(__file__)
sys.path.append(_path)


class Interface(threading.Thread):
    def __init__(self, API, IF):
        threading.Thread.__init__(self)
        self.API = API
        self.IF = IF
        self.name = IF.IFName

    def run(self):
        self.IF.init()


class InterfaceRunner():
    interfaces = {}
    def __init__(self):
        password_path = os.path.join(os.path.dirname(os.path.abspath('')), 'IFM_passwords.txt')
        if not os.path.exists(password_path):
            sys.stderr.write('Warning! The config file is absent! Some interface can have exceptions!\nThe config file: %s\n' % password_path)
            self.conf = {}
        else: #self.conf = conftools.loadconf(password_path)
            with open(password_path, 'r') as f:
                self.conf = json.load(f)

    def turnOnInterface(self, api, Settings, IFNames):

        for IFName in IFNames:
            self.interfaces[IFName] = [None, None]
            IFModule = Settings.modules['interface'][IFName]
            IFClass = IFModule.Interface(api, Settings, self.conf.get(IFName))

            IFClass.IFName = IFName
            self.interfaces[IFName][1] = IFClass
            t = Interface(api, IFClass)  # threading.Thread(target=IFClass.init)

            # t.daemon = True
            t.start()
            self.interfaces[IFName][0] = t
        print('Count of processes:', threading.activeCount())

    def turnOffInterface(self, IFNames):
        for IFName in IFNames:
            if IFName in IFNames:
                del self.interfaces[IFName]
            else:
                print('Interface \"%s\" doesn\'t deleted because it\'s absent.' % IFName)
