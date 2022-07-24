import os

from manspy.utils.settings import DEFAULT_PATH_MODULES, Settings, InitSettings
from interface.runner import InterfaceRunner

Settings(paths_import=[('interface', os.path.join(DEFAULT_PATH_MODULES, 'interface'))])
interfaces = (  # кортежи вида: (вкл/выкл, аргументы настроек, имя модуля интерфейса)
    (1, {}, 'autofeed'),  # Автоподатчик предложений - для теста, но можно писать "скрипты"
    (0, {}, 'tkinter'),
    (0, {}, 'jabber'),
    (0, {}, 'vkcom'),
    (0, {}, 'commandline'),
    (0, {}, 'telegram'),
)
interfaces = [(i[1], i[2]) for i in interfaces if i[0]]
with InitSettings():
    interface_runner = InterfaceRunner()
    interface_runner.turn_on_interface(interfaces)
