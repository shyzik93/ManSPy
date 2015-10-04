# -*- coding: utf-8 -*-
""" Модуль параллельно запускает все МИ.
    Цикл приёма сообщения от ИСУ необходимо реализовывать внутри МИ.
    Запрещено называть МИ следующими именами: all, general.

    Модуль запускаются через потоки, поэтому при зависании одного модуля встанет вся программа, например при вызове input().
    Чтобы устранить эту проблему, нужно запускать каждый МИ как отдельный процесс (прграмму), но появляется задача: как передать объект класса API/
"""

import os, sys, threading

_path = os.path.dirname(__file__)
sys.path.append(_path)

password_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(''))), 'IFM_passwords.txt')
def get_passwords(password_path, password_dict):
  with open(password_path, 'r') as f:
    password_strings = f.read().split('\n')
  for s in password_strings:
    if not s or s[0] == '#': continue
    name, value = s.split(':')
    password_dict[name.strip()] = [v.strip() for v in value.strip().split(' ')]

class Interfaces():
  interfaces = {}
  def __init__(self, API, *IFNames):
    self.password_dict = {}
    get_passwords(password_path, self.password_dict)
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
      if IFName in self.password_dict: IFModule.passwords = self.password_dict[IFName]
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
