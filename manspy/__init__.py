""" Предоставляет API интеллекта, который используется модулями интерфейса.
    В качестве API:
      API = ISM.API(Settings) # Settings - словарь, задающий настройки.
    Примеры возможных интерфейсов: текстовый чат, распознаватель речи,
    мессенджеры, интерфейс мозг-компьютер, приёмник звонков и SMS и так далее.
"""
import sqlite3 as sql
import time, sys, os, copy, json, datetime
from . import import_action
from .analyse_text import LangClass
from manspy.utils.settings import Settings

from . import message

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
        IF.settings = self.Settings(**IF.settings)
        IF.settings.db_sqlite3 = create_bd_file(IF.settings.language, 'main_data.db')
        IF.init()

    def import_all_modules(self):
        import importlib, pkgutil

        #module_dir = self.paths_import['language']
        #for module_file_name in os.listdir(module_dir):
        #    if module_file_name.startswith('language_'):
        #        module_path = os.path.join(module_dir, module_file_name)
        #        module = importlib.import_module(module_path)
        #        print(module)

        for module_type, path_import in self.paths_import:
            if module_type == 'language':

                for module_info in pkgutil.iter_modules(path=[path_import]):
                    if module_info.name.startswith('language_'):
                        module = module_info.module_finder.find_module(module_info.name).load_module()
                        module_code = module_info.name
                        self.Settings.set_module('language', module, module_code[9:])

            elif module_type == 'logger':

                for module_info in pkgutil.iter_modules(path=[path_import]): 
                    if module_info.name.startswith('logger_'):
                        module = module_info.module_finder.find_module(module_info.name).load_module()
                        module_code = module_info.name
                        class_name = ''.join([subname.capitalize() for subname in module_code.split('_')])
                        self.Settings.set_module('logger', getattr(module, class_name)(), module_code[7:])

    def import_fasifs(self, language, settings):
        print("Import fasifs for {0} language...".format(language))
        t1 = time.time()

        self.action_importer.import_for_lang(language, settings)

        print('  ', time.time() - t1)

    def __init__(self):
        self.Settings = Settings
        
        default_path_modules = os.path.dirname(os.path.dirname(__file__))
        self.paths_import = [
            ('language', os.path.join(default_path_modules, 'manspy', 'NLModules')),
            ('logger', os.path.join(default_path_modules, 'logger')),
        ]

        self.Settings.dir_db = self.make_db_dir(self.Settings.dir_db)
        self.import_all_modules()
        print(self.Settings.modules)

        """ Инициализация ManSPy """
        #settings = copy.deepcopy(self.default_settings)
        #self.update_settings_for_IF(settings)
        # Меняем настройки по умолчанию на пользовательские

        print("Init nature language's module...")
        t1 = time.time()
        self.LangClass = LangClass()
        t2 = time.time()
        print('  ', t2 - t1)
        
        print("Init action's modules...")
        t1 = time.time()
        self.action_importer = import_action.ImportAction(self.LangClass, self.Settings.assoc_version)
        #self.action_importer.fsf2json()
        self.was_imported = {}
        t2 = time.time()
        print('  ', t2 - t1)

        for language in self.Settings.modules['language']:
            self.import_fasifs(language, self.Settings(language=language))

        #print("Init functions's module...")
        #t1 = time.time()
        #self.LogicShell = FCModule.LogicShell()
        #t2 = time.time()
        #print('  ', t2 - t1)
        print("Ready!")

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
