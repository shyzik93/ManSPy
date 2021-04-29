""" Предоставляет API интеллекта, который используется модулями интерфейса.
    В качестве API:
      API = ISM.API(Settings) # Settings - словарь, задающий настройки.
    Примеры возможных интерфейсов: текстовый чат, распознаватель речи,
    мессенджеры, интерфейс мозг-компьютер, приёмник звонков и SMS и так далее.
"""
import os

from manspy.analyse_text import nature2internal
from manspy.utils.settings import Settings
from manspy.utils import importer
from manspy.message import Message
from manspy.fasif.parser import fasif_parser


class MainException(Exception):
    pass


DEFAULT_PATH_MODULES = os.path.dirname(os.path.dirname(__file__))
DEFAULT_PATHS_IMPORT = [
    ('language', os.path.join(DEFAULT_PATH_MODULES, 'language')),  # модуль языка должен быть перед модулем действий
    ('logger', os.path.join(DEFAULT_PATH_MODULES, 'logger')),
    ('action', os.path.join(DEFAULT_PATH_MODULES, 'action')),
]


class API:
    def __init__(self, paths_import=None, current_work_dir=None):
        self.paths_import = DEFAULT_PATHS_IMPORT + (paths_import if paths_import else [])

        if current_work_dir is None:
            current_work_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            current_work_dir = os.path.join(current_work_dir, 'LOGS')
        if not os.path.exists(current_work_dir) or not os.path.isdir(current_work_dir):
            os.mkdir(current_work_dir)
        os.chdir(current_work_dir)

        Settings.c, Settings.cu = importer.database(Settings.db_type)(Settings.db_settings[Settings.db_type])

    def send_to_in(self, w_text, settings, any_data=None):
        """any_data - any data, if you would like to pass it to IF with answer."""
        #print(threading.current_thread().name)

        if w_text:
            message = Message(settings, any_data, w_text, 'W')
            return message, nature2internal(message)

    def __enter__(self):
        for module_type, path_import in self.paths_import:
            if module_type == 'action':
                fasif_parser(path_import, Settings(history=False))
            else:
                for module, module_code in importer.import_modules(path_import, module_type):
                    if module_type == 'logger':
                        module = module.Logger()

                    Settings.set_module(module_type, module, module_code)

        return self

    def __exit__(self, Type, Value, Trace):

        Settings.c.close()
        for module_code, module in Settings.modules['logger'].items():
            module.close()

        if Type is None:  # Если исключение не возникло
            pass
        else:             # Если возникло исключение
            return False  # False - исключение не обработано
                          # True  - исключение обработано
