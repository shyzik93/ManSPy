#! /usr/bin/env python
# -*- coding: utf-8 -*-
import private_data, ManSPy, IFModules

Settings = {
  'logic': True,
  'convert2IL': True,
  'test': True,
  'storage_version': 2, # (1, 2) версия БД (слова, их отношения, ФАСИФы)
  'assoc_version': 3 # (2, 3) версия способа ассоциирования лингвистических и технических данных (ФАСИФа)
  }
interfaces = { # 1 - on, 0 - off
  'autofeed':    1, # Автоподатчик предложений - для теста, но можно писать "скрипты"
  'TKinter':     1,
  'jabber':      0,
  'vkcom':       0, # с ошибками
  'Commandline': 0  # не имеет смысла
  }
interfaces = [i for i in interfaces if interfaces[i]]

API = ManSPy.API(Settings)
IF = IFModules.Interfaces(API, private_data.IFM_settings, *interfaces)