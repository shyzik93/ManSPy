# -*- coding: utf-8 -*-
import ManSPy, IFModules, sys
sys.dont_write_bytecode = True # можно удалить для ускорения работы

Settings = {
  'logic': True,
  'convert2IL': True,
  'test': True,
  'storage_version': 2, # (1, 2) версия хранилища данных (слова, их отношения, ФАСИФы)
  'assoc_version': 2 # (2, 3) версия способа ассоциирования лингвистических и технических данных (ФАСИФа)
  }
interfaces = {
  'autofeed':    1, # Автоподатчик предложений - для теста, но можно писать "скрипты"
  'TKinter':     1,
  'jabber':      0,
  'vkcom':       0, # с ошибками
  'Commandline': 0  # не имеет смысла
  }
interfaces = [i for i in interfaces if interfaces[i]]

API = ManSPy.API(Settings)
IF = IFModules.Interfaces(API, *interfaces)
