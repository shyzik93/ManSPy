#!/usr/bin/env python3
from manspy import API, InterfaceRunner, Settings

interfaces = {  # 1 - on, 0 - off
  'autofeed':    0,  # Автоподатчик предложений - для теста, но можно писать "скрипты"
  'tkinter':     0,
  'jabber':      0,
  'vkcom':       0,  # с ошибками
  'commandline': 1,
  'telegram':    0,
  }
interfaces = [i for i in interfaces if interfaces[i]]

with API() as api:
    interface_runner = InterfaceRunner()
    interface_runner.turnOnInterface(api, Settings, interfaces)
