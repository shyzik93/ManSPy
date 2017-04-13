#! /usr/bin/env python
# -*- coding: utf-8 -*-
import ManSPy, IFModules

interfaces = { # 1 - on, 0 - off
  'autofeed':    1, # Автоподатчик предложений - для теста, но можно писать "скрипты"
  'TKinter':     1,
  'jabber':      0,
  'vkcom':       0, # с ошибками
  'Commandline': 0  # не имеет смысла
  }
interfaces = [i for i in interfaces if interfaces[i]]

# Анализ и выпорлнение сообщений
API = ManSPy.API()
# Приём сообщения от пользователя и возврат ответа
IF = IFModules.Interfaces()
IF.turnOnInterface(API, *interfaces)