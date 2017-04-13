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