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

password_path = os.path.join(os.path.dirname(os.path.abspath('')), 'IFM_passwords.txt')

class Interfaces():
  interfaces = {}
  def __init__(self, API, *IFNames):
    if not os.path.exists(password_path):
      sys.stderr.write('Warning! The config file is absent! Some interfaces can have exceptions!\nThe config file: %s\n' % password_path)
      self.conf = {}
    else: #self.conf = conftools.loadconf(password_path)
      with open(password_path, 'r') as f: self.conf = json.load(f)

    self.API = API
    self.turnOnInterface(*IFNames)

  def turnOnInterface(self, *IFNames):
    for IFName in IFNames:
      """IFModule = __import__(IFName)
      IFModule.IFName = IFName
      IFModule.API = self.API
      t = threading.Thread(target=IFModule.run)
      t.setName(IFName)
      t.daemon = True
      t.start()
      self.interfaces[IFName] = t"""
      IFModule = __import__('IFM_'+IFName)
      IFModule.IFName = IFName
      if IFName in self.conf: IFModule.passwords = self.conf[IFName]
      self.interfaces[IFName] = [None, None]
      if 'Interface' in dir(IFModule):
        IFClass = IFModule.Interface(self.API)
        self.interfaces[IFName][1] = IFClass
        t = threading.Thread(target=IFClass.init)
      else:
        IFModule.API = self.API
        self.interfaces[IFName][1] = IFModule
        t = threading.Thread(target=IFModule.init)
      t.setName(IFName)
      #t.daemon = True
      t.start()
      print 'Processes info:', threading.activeCount()
      self.interfaces[IFName][0] = t

  def turnOffInterface(self, *IFNames):
    for IFName in IFNames:
      if IFName in IFNames:
        del self.interfaces[IFName]
      else: print 'Interface \"%s\" doesn\'t deleted because it\'s absent.' % IFName
