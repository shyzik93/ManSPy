# -*- coding: utf-8 -*-
""" Модуль параллельно запускает все МИ.
    Цикл приёма сообщения от ИСУ необходимо реализовывать внутри МИ.
    Запрещено называть МИ следующими именами: all, general.

    Модуль запускаются через потоки, поэтому при зависании одного модуля встанет вся программа, например при вызове input().
    Чтобы устранить эту проблему, нужно запускать каждый МИ как отдельный процесс (прграмму), но появляется задача: как передать объект класса API/
"""
#import repper, conftools
import os, sys, threading, json

_path = os.path.dirname(__file__)
sys.path.append(_path)

class Interface(threading.Thread):
    def __init__(self, API, IF):
        threading.Thread.__init__(self)
        self.API = API
        self.IF = IF
        self.name = IF.IFName

    def run(self):
        self.API.init_interface(self.IF)

class Interfaces():
    interfaces = {}
    def __init__(self):
        password_path = os.path.join(os.path.dirname(os.path.abspath('')), 'IFM_passwords.txt')
        if not os.path.exists(password_path):
            sys.stderr.write('Warning! The config file is absent! Some interfaces can have exceptions!\nThe config file: %s\n' % password_path)
            self.conf = {}
        else: #self.conf = conftools.loadconf(password_path)
            with open(password_path, 'r') as f: self.conf = json.load(f)

    def turnOnInterface(self, API, *IFNames):

        for IFName in IFNames:

            IFModule = __import__('IFM_'+IFName)
            if IFName in self.conf: IFModule.passwords = self.conf[IFName]
            self.interfaces[IFName] = [None, None]

            if 'Interface' in dir(IFModule):
                IFClass = IFModule.Interface(API)
                IF = IFClass
            else:
                IFModule.API = API
                IF = IFModule

            IF.IFName = IFName
            if 'settings' not in dir(IF): IF.settings = None
            self.interfaces[IFName][1] = IF
            t = Interface(API, IF)#threading.Thread(target=IF.init)

            #t.daemon = True
            t.start()
            self.interfaces[IFName][0] = t
        print('Count of processes:', threading.activeCount())

    def turnOffInterface(self, *IFNames):
        for IFName in IFNames:
            if IFName in IFNames:
                del self.interfaces[IFName]
            else: print('Interface \"%s\" doesn\'t deleted because it\'s absent.' % IFName)
