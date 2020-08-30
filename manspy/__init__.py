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
    default_settings = {'history': True,
              'monitor': True, # включает вывод на экран статистику работы ИСУ
              'logic': True, # включает модуль логики
              'convert2IL': True, # включает последний этап конвертации
                               # если при отключении включёна логика, то будет ошибка
              'language': 'Esperanto',
              'test': True, # тестовый режим, включаемый в процессе отладки и разработки
              'read_text': None, # функция, в котору manspy пишет ответ.
              'ifname': '', # уникальное имя интерфейса. Необходимо для журналов.

              # не рекомендуемые к изменению
              'log_all': True,
              'storage_version': 2,
              'assoc_version': 3,
              'dir_db': None,
              'db_sqlite3': None,
    }

    def make_db_dir(self, db_path=None):
        # Устанавливаем путь к директории базы данных как рабочую (текущую)
        if db_path is None: db_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(db_path, 'DATA_BASE')
        if not os.path.exists(db_path) or not os.path.isdir(db_path):
            os.mkdir(db_path)
        os.chdir(db_path)
        return db_path

    def update_settings_for_IF(self, settings):
        # Проверяем правильность ключей
        keys = self.default_settings.keys()
        for user_key in settings.keys():
            if user_key not in keys:
                raise MainException('error2: Wrong name of key in settings: %s' % str(user_key))
        # Обновляем настройки
        _settings = copy.deepcopy(self.default_settings) # Создаём новые настройки. Только при инициализации даннгого класса в модуле run.py
        _settings.update(settings)
        settings.update(_settings)
        # Корректируем настройки
        settings['language'] = settings['language'].capitalize()
        settings['db_sqlite3'] = create_bd_file(settings['language'], 'main_data.db')

    def import_module(self, module_type, module_name):
        if module_type == 'action':
            module = importlib.import_module('manspy.Action.{module_name}')
        elif module_type == 'interface':
            module = None
        elif module_type == 'language':
            module = importlib.import_module('manspy.NLModules.{module_name}')
        elif module_type == 'logger':
            module = None

    def add_module(self, module_type, module, module_code=None):
        if isinstance(self.modules[module_type], list):
            self.modules[module_type].append(module)
        elif isinstance(self.modules[module_type], dict):
            self.modules[module_type][module_code] = module
    
    def import_all_modules(self):
        import importlib, pkgutil
        
        #module_dir = self.paths_import['language']
        #for module_file_name in os.listdir(module_dir):
        #    if module_file_name.startswith('language_'):
        #        module_path = os.path.join(module_dir, module_file_name)
        #        module = importlib.import_module(module_path)
        #        print(module)

        for module_info in pkgutil.iter_modules(path=[self.paths_import['language']]):
            if module_info.name.startswith('language_'):
                module = module_info.module_finder.find_module(module_info.name).load_module()
                self.add_module('language', module, module_info.name.split('_')[-1].capitalize())


    def import_fasifs(self, settings):
        print("Import fasifs for {0} language...".format(settings['language']))
        t1 = time.time()

        self.action_importer.import_for_lang(settings)
        self.was_imported[settings['language']] = True

        print('  ', time.time() - t1)

    def __init__(self):
        self.modules = {
            'language': {},
            'logger': [],
        }
        
        default_path_modules = os.path.dirname(os.path.dirname(__file__))
        self.paths_import = {
            'language': os.path.join(default_path_modules, 'manspy', 'NLModules')
        }

        #self.default_settings['modules'] = self.modules
        self.default_settings['dir_db'] = self.make_db_dir(self.default_settings['dir_db'])
        
        self.import_all_modules()
        print(self.modules)
        #exit()

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
        self.action_importer = import_action.ImportAction(self.LangClass, self.default_settings['assoc_version'])
        #self.action_importer.fsf2json()
        self.was_imported = {}
        t2 = time.time()
        print('  ', t2 - t1)

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

        if settings['language'] not in self.was_imported:
            self.import_fasifs(settings)

        if w_text:
            w_msg = message.Message(settings, text_settings, w_text, 'W')
            return w_msg, self.LangClass.NL2IL(w_msg)
