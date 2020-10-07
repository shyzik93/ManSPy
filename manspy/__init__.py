""" Предоставляет API интеллекта, который используется модулями интерфейса.
    В качестве API:
      API = ISM.API(Settings) # Settings - словарь, задающий настройки.
    Примеры возможных интерфейсов: текстовый чат, распознаватель речи,
    мессенджеры, интерфейс мозг-компьютер, приёмник звонков и SMS и так далее.
"""
import sqlite3 as sql
import time
import os

from manspy.analyse_text import LangClass
from manspy.utils.settings import Settings
from manspy.utils import importer
from manspy import message
from manspy.fasif.parser import FASIFParser

sql.enable_callback_tracebacks(True)


def create_bd_file(language, name):
    if not os.path.exists(language) or not os.path.isdir(language):
        os.mkdir(language) # хдесь бывает ошибка, так, видимо, эта функция вызывается параллельно где-то в другом потоке
    name = os.path.join(language, name)
    c = sql.connect(name)
    c.row_factory = sql.Row
    cu = c.cursor()
    return c, cu


class MainException(Exception): pass


class API():
    # настройки задаются один раз. Но можно написать модуль для изменения
    # настроек через канал общения.

    def make_db_dir(self, db_path=None):
        # Устанавливаем путь к директории базы данных как рабочую (текущую)
        if db_path is None: db_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(db_path, 'DATA_BASE')
        if not os.path.exists(db_path) or not os.path.isdir(db_path):
            os.mkdir(db_path)
        os.chdir(db_path)
        return db_path

    def init_interface(self, IF):
        IF.settings = Settings(**IF.settings)
        IF.settings.db_sqlite3 = create_bd_file(IF.settings.language, 'main_data.db')
        IF.init()

    def __init__(self):
        default_path_modules = os.path.dirname(os.path.dirname(__file__))
        self.paths_import = [
            ('language', os.path.join(default_path_modules, 'manspy', 'NLModules')),  # обязательно первые в списке
            ('logger', os.path.join(default_path_modules, 'logger')),
            ('action', os.path.join(default_path_modules, 'action')),
        ]

        Settings.dir_db = self.make_db_dir(Settings.dir_db)

        self.LangClass = LangClass()
        fasif_parser = FASIFParser(self.LangClass)
        #self.action_importer.fsf2json()
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

        """ Инициализация ManSPy """
        #settings = copy.deepcopy(self.default_settings)
        #self.update_settings_for_IF(settings)
        # Меняем настройки по умолчанию на пользовательские

        #self.LogicShell = FCModule.LogicShell()

    def write_text(self, w_text, settings, text_settings=None):
        '''
            any_data - any data, if you would like to pass it to IF with answer.
        '''
        #print(threading.current_thread().name)

        if text_settings is None: text_settings = {}
        if 'any_data' not in text_settings: text_settings['any_data'] = None
        if 'levels' not in text_settings: text_settings['levels'] = "graphmath exec"
        if 'print_time' not in text_settings: text_settings['print_time'] = True

        if w_text:
            w_msg = message.Message(settings, text_settings, w_text, 'W')
            return w_msg, self.LangClass.NL2IL(w_msg)
