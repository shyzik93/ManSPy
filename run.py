#!/usr/bin/env python3
import manspy

interfaces = {  # 1 - on, 0 - off
  'autofeed':    1,  # Автоподатчик предложений - для теста, но можно писать "скрипты"
  'TKinter':     0,
  'jabber':      0,
  'vkcom':       0,  # с ошибками
  'Commandline': 0,  # не имеет смысла
  'telegram':    0,
  }
interfaces = [i for i in interfaces if interfaces[i]]

# Анализ и выполнение сообщений
api = manspy.API()
# Приём сообщения от пользователя и возврат ответа
interface_runner = manspy.InterfaceRunner()
interface_runner.turnOnInterface(api, *interfaces, settings)
