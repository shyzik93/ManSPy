""" Предоставляет API интеллекта, который используется модулями интерфейса.
    В качестве API:
      API = ISM.API(Settings) # Settings - словарь, задающий настройки.
    Примеры возможных интерфейсов: текстовый чат, распознаватель речи,
    мессенджеры, интерфейс мозг-компьютер, приёмник звонков и SMS и так далее.
"""
import os

from manspy.analyse_text import LangClass
from manspy.utils.settings import Settings
from manspy.utils import importer
from manspy.message import Message
from manspy.fasif.parser import FASIFParser


class MainException(Exception):
    pass


class API:
    def __init__(self, current_work_dir=None):
        default_path_modules = os.path.dirname(os.path.dirname(__file__))
        self.paths_import = [
            ('language', os.path.join(default_path_modules, 'manspy', 'NLModules')),  # обязательно первые в списке
            ('logger', os.path.join(default_path_modules, 'logger')),
            ('action', os.path.join(default_path_modules, 'action')),
        ]

        if current_work_dir is None:
            current_work_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            current_work_dir = os.path.join(current_work_dir, 'LOGS')
        if not os.path.exists(current_work_dir) or not os.path.isdir(current_work_dir):
            os.mkdir(current_work_dir)
        os.chdir(current_work_dir)

        Settings.c, Settings.cu = importer.database(Settings.db_type)(Settings.db_settings[Settings.db_type])

        self.LangClass = LangClass()
        fasif_parser = FASIFParser(self.LangClass)
        self.was_imported = {}

        for module_type, path_import in self.paths_import:
            #for module, module_code in getattr(importer, module_type)(path_import):
            #    Settings.set_module(module_type, module, module_code)
            if module_type == 'language':
                for module, module_code in importer.language(path_import):
                    Settings.set_module(module_type, module, module_code)
            elif module_type == 'logger':
                for module, module_code in importer.logger(path_import):
                    Settings.set_module(module_type, module, module_code)
            elif module_type == 'action':
                # TODO: функция fasif_parser.parse должна импоттировать лингв. информацию для всех языков, для которых импортированы языковые модули.
                # TODO: функция fasif_parser.parse должна принять только path_import
                for language in Settings.modules['language']:
                    fasif_parser.parse(path_import, language, Settings(language=language))

    def write_text(self, w_text, settings, _text_settings=None):
        """any_data - any data, if you would like to pass it to IF with answer."""
        #print(threading.current_thread().name)

        _text_settings = _text_settings or {}
        text_settings = {
            'any_data': _text_settings.get('any_data'),
            'levels': _text_settings.get('levels', 'graphmath exec'),
            'print_time': _text_settings.get('print_time', True)
        }

        if w_text:
            message = Message(settings, text_settings, w_text, 'W')
            return message, self.LangClass.NL2IL(message)
