#!/usr/bin/env python3
from manspy import API, InterfaceRunner, Settings

interfaces = {  # 1 - on, 0 - off
  'autofeed':    1,  # Автоподатчик предложений - для теста, но можно писать "скрипты"
  'TKinter':     0,
  'jabber':      0,
  'vkcom':       0,  # с ошибками
  'Commandline': 0,  # не имеет смысла
  'telegram':    0,
  }
interfaces = [i for i in interfaces if interfaces[i]]

api = API()
interface_runner = InterfaceRunner()
interface_runner.turnOnInterface(api, Settings, interfaces)
