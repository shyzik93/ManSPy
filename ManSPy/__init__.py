# -*- coding: utf-8 -*-
""" Предоставляет API интеллекта, который используется модулями интерфейса.
    В качестве API:
      API = ISM.API(Settings) # Settings - словарь, задающий настройки.
    Примеры возможных интерфейсов: текстовый чат, распознаватель речи,
    мессенджеры, интерфейс мозг-компьютер, приёмник звонков и SMS и так далее.
"""
import time, sys, os, copy, threading
from . import FCModule, import_action
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

    def __init__(self, IF, direction=None, text=None, any_data=None):
        self.IF = IF
        self.r_texts = []

        if direction == 'W': self.from_IF(text)
        elif direction == 'R': self.to_IF(text)

        self.any_data = any_data

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
        self.IF.read_text(r_text, self.any_data)

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
              'test': True, # тестовый режим, включаемый в процессе отладки и разработки

              # не рекомендуемые к изменению
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

    def __init__(self):
        self.default_settings['dir_db'] = self.make_db_dir(self.default_settings['dir_db'])

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

        print("Init functions's module...")
        t1 = time.time()
        self.LogicShell = FCModule.LogicShell()
        t2 = time.time()
        print('  ', t2 - t1)
        print("Ready!")

    def write_text(self, IF, w_text, any_data=None):
        '''
            any_data - any data, if you would like to pass it to IF with answer.
        '''
        #print(threading.current_thread().name)

        if IF.settings['language'] not in self.was_imported:

            print("Import fasifs for {0} language...".format(IF.settings['language']))
            t1 = time.time()

            self.action_importer.import_for_lang(IF.settings)
            self.was_imported[IF.settings['language']] = True

            t2 = time.time()
            print('  ', t2 - t1)

        w_msg = Message(IF, 'W', w_text, any_data)
        if w_text:
            t =time.time()
            w_msg.ils = self.LangClass.NL2IL(w_msg)
            w_msg.time_total = time.time()-t
            print('    Total: ', w_msg.time_total)
            ExecError = self.LogicShell.execIL(w_msg)
            return w_msg