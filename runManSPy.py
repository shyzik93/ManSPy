# !usr/bin/python
# -*- coding: utf-8 -*-
import ManSPy, IFModules

Settings = {
  'logic': True,
  'convert2IL': True,
  'test': True,
  'storage_version': 2, # (1, 2) версия БД (слова, их отношения, ФАСИФы)
  'assoc_version': 3 # (2, 3) версия способа ассоциирования лингвистических и технических данных (ФАСИФа)
  }
'''
Поддерживаемые комбинации версий:
БД | Ассоц. | Хронология
-------------------------
 1 |   2    |    1
 1 |   3    |      не использовалась
 2 |   2    |    2 текущая
 2 |   3    |    3 в разработке
'''
interfaces = {
  'autofeed':    1, # Автоподатчик предложений - для теста, но можно писать "скрипты"
  'TKinter':     0,
  'jabber':      0,
  'vkcom':       0, # с ошибками
  'Commandline': 0  # не имеет смысла
  }
interfaces = [i for i in interfaces if interfaces[i]]

API = ManSPy.API(Settings)
IF = IFModules.Interfaces(API, *interfaces)
