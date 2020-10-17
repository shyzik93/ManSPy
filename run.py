#!/usr/bin/env python3
import manspy
import ifmodules

interfaces = {  # 1 - on, 0 - off
  'autofeed':    1,  # Автоподатчик предложений - для теста, но можно писать "скрипты"
  'TKinter':     0,
  'jabber':      0,
  'vkcom':       0,  # с ошибками
  'Commandline': 0,  # не имеет смысла
  'telegram': 1,
  }
interfaces = [i for i in interfaces if interfaces[i]]

# Анализ и выпорлнение сообщений
API = manspy.API()
# Приём сообщения от пользователя и возврат ответа
IF = ifmodules.Interfaces()
IF.turnOnInterface(API, *interfaces)
