import os

from manspy import API, DEFAULT_PATH_MODULES, InterfaceRunner, Settings

interfaces = {  # 1 - on, 0 - off
  'autofeed':    0,  # Автоподатчик предложений - для теста, но можно писать "скрипты"
  'tkinter':     0,
  'jabber':      0,
  'vkcom':       0,  # с ошибками
  'commandline': 1,
  'telegram':    0,
  }
interfaces = [i for i in interfaces if interfaces[i]]

paths_import = [('interface', os.path.join(DEFAULT_PATH_MODULES, 'interface'))]

with API(paths_import) as api:
    interface_runner = InterfaceRunner()
    interface_runner.turn_on_interface(api, Settings, interfaces)
