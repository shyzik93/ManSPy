# -*- coding: utf-8 -*-
""" Предоставляет API интеллекта, который используется модулями интерфейса.
    В качестве API:
      API = ISM.API(Settings) # Settings - словарь, задающий настройки.
    Примеры возможных интерфейсов: текстовый чат, распознаватель речи,
    мессенджеры, интерфейс мозг-компьютер, приёмник звонков и SMS и так далее.
"""
from . import FCModule, import_action, message
import time, sys, os, copy
from .analyse_text import LangClass

import sqlite3 as sql

sql.enable_callback_tracebacks(True)

def create_bd_file(language, name):
    if not os.path.exists(language) or not os.path.isdir(language):
        os.mkdir(language)
    name = os.path.join(language, name)
    c = sql.connect(name)
    c.row_factory = sql.Row
    cu = c.cursor()
    return c, cu

class MainException(Exception): pass

# -*- coding: utf-8 -*-

import time, json

class Message:

    ''' Создан пока только для: логирования с учётом уникального номера сообщения; передачи настроек текущего потока '''

    def __init__(self, IF):
        self.IF = IF
        self.r_texts = []
        '''self.settings = settings
        self.direction = direction
        self.nl = message_nl # nl = Nature Language
        self.il = None # il = Internal Language

        self.c, self.cu = self.settings['db_sqlite3']

        self.cu.execute(\'''
        CREATE TABLE IF NOT EXISTS `log_history` (
          `message_id` INTEGER PRIMARY KEY AUTOINCREMENT,
          `direction` TEXT,
          `thread_name` VARCHAR(255),
          `language` INTEGER,
          `date_add` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `message_nl` TEXT,
          `message_il` JSON,
          `a_graphemath` JSON,
          `a_morph` JSON,
          `a_postmorph` JSON,
          `a_synt` JSON);
      \''')

        t1 = time.time()
        self.cu.execute(
          'INSERT INTO `log_history` (`direction`, `thread_name`, `language`, `message_nl`) VALUES (?, ?, ?, ?);',
          (self.direction, self.settings['thread_name'], self.settings['language'], self.nl)
        )
        t2 = time.time()
        _t1 = t2 - t1
        self.c.commit()
        t3 = time.time()
        _t2 = t3 - t2
        #print(_t1, _t2)


        self.message_id = self.cu.lastrowid
        #print(self.message_id)"""
        '''

    def _save_history(self, text, Type):
        if text:
            Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()-time.altzone))
            if Type == 'R': text = '   '+text
            text = "* %s  %s  %s: %s\n" % (Type, Time, self.IF.IFName, text)
            with open('history.txt', 'ab') as f: f.write(bytearray(text, 'utf-8'))

    def toString(self, r_text):
        if isinstance(r_text, (int, float, complex)): return str(r_text)
        else: return r_text

    def to_IF(self, r_text):
        r_text = self.toString(r_text)
        if self.IF.settings['history']: self._save_history(r_text, "R")
        self.IF.to_IF(r_text)

    def from_IF(self, w_text):
        self.w_text = w_text
        if self.IF.settings['history']: self._save_history(w_text, "W")

    def log(self, row_name, row_value):
        #if isinstance(row_value, (dict, list)): row_value = json.dumps(row_value)
        #self.cu.execute('UPDATE `log_history` SET `'+row_name+'`=? WHERE `message_id`=?', (row_value, self.message_id));
        #self.c.commit()
        pass

class API():
    # настройки задаются один раз. Но можно написать модуль для изменения
    # настроек через канал общения.
    default_settings = {'history': True,
              'monitor': True, # включает вывод на экран статистику работы ИСУ
              'logic': True, # включает модуль логики
              'convert2IL': True, # включает последний этап конвертации
                               # если при отключении включёна логика, то будет ошибка
              'language': 'Esperanto',
              'storage_version': 2,
              'assoc_version': 3,
              'test': True, # тестовый режим, включаемый в процессе отладки и разработки
              'dir_db': None,
              'db_sqlite3': None,
              'thread_name': None
    }

    settings = {}

    def make_db_dir(self, dir_db=None):
        # Устанавливаем путь к директории базы данных как рабочую (текущую)
        if dir_db is None: db_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        else: db_path = dir_db
        db_path = os.path.join(db_path, 'DATA_BASE')
        if not os.path.exists(db_path) or not os.path.isdir(db_path):
            os.mkdir(db_path)
        os.chdir(db_path)
       return dir_db

    def update_settings_for_IF(self, settings):
        ''' Здесь инициализируется то, что не может быть создано в одном потоке, а использовано в другом.
            Например, объект соединения с базой.
        '''

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
        settings['dir_db'] = self.make_db_dir(settings['dir_db'])
        settings['db_sqlite3'] = create_bd_file(settings['language'], 'main_data.db')

    def __init__(self):
        """ Инициализация ManSPy """
        settings = copy.deepcopy(self.default_settings)
        self.update_settings_for_IF(settings)
        # Меняем настройки по умолчанию на пользовательские
        print("Load action's modules...")
        t1 = time.time()
        Import = import_action.ImportAction(settings)
        Import.importAll()
        t2 = time.time()
        print('  ', t2 - t1)
        print("Load nature language's module...")
        t1 = time.time()
        self.LangClass = LangClass(settings)
        t2 = time.time()
        print('  ', t2 - t1)
        print("Init executing functions's module...")
        t1 = time.time()
        self.LogicShell = FCModule.LogicShell()
        t2 = time.time()
        print('  ', t2 - t1)
        print("Ready!")

    def write_text(self, IF, w_text):
        #print 'write', type(w_text)
        w_msg = message.Message(IF)
        if w_text:
            w_msg.from_IF(w_text)
            _ILs = self.LangClass.NL2IL(w_msg)
            w_msg.ils = _ILs
            #self.print_errors(ErrorConvert)
            ExecError = self.LogicShell.execIL(w_msg)