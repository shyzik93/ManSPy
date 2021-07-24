import os

from manspy.utils.settings import DEFAULT_PATH_MODULES, Settings, InitSettings
from manspy import InterfaceRunner

Settings(paths_import=[('interface', os.path.join(DEFAULT_PATH_MODULES, 'interface'))])
interfaces = (
    (1, Settings(), 'autofeed'),  # Автоподатчик предложений - для теста, но можно писать "скрипты"
    (0, Settings(), 'tkinter'),
    (0, Settings(), 'jabber'),
    (0, Settings(), 'vkcom'),
    (0, Settings(), 'commandline'),
    (0, Settings(), 'telegram'),
)
interfaces = [(i[1], i[2]) for i in interfaces if i[0]]
with InitSettings():
    interface_runner = InterfaceRunner()
    interface_runner.turn_on_interface(interfaces)
