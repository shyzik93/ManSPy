# -*- coding: utf-8 -*-
import ManSPy, IFModules

Settings = {
  'logic': 1,
  'convert2IL': 1,
  'test': 1,
  'storage_version': 2
  }
interfaces = {
  'autofeed':    1,
  'TKinter':     0,
  'jabber':      0,
  'vkcom':       0, # с ошибками
  'Commandline': 0  # не имеет смысла
  }
interfaces = [i for i in interfaces if interfaces[i]]

API = ManSPy.API(Settings)
IF = IFModules.Interfaces(API, *interfaces)
