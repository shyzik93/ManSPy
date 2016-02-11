# -*- coding: utf-8 -*-
""" Предоставляет API интеллекта, который используется модулями интерфейса.
    В качестве API:
      API = ISM.API(Settings) # Settings - словарь, задающий настройки.
      Answer = API.Asker(Question) # Asker - функция, принимающая вопрос
      и возвращающая ответ. Функция может возвращать информацию, которая
      не была запрошена, то есть необходимо постоянно вызывать эту функцию,
      передавая ей пустую строку (или вопрос), для получения такой информации.
    Примеры возможных интерфейсов: текстовый чат, распознаватель речи,
    мессенджеры, интерфейс мозг-компьютер, приёмник звонков и SMS и так далее.
"""
import repper, simpletools
import FCModule, import_action, common, time, codecs, sys, os
from analyse_text import LangClass

class MainException(Exception): pass

def _save_history(text, Type, IFName):
  if text:
    Time = time.strftime('%c', time.gmtime(time.time()-time.altzone))
    if Type == 'R': text = '   '+text
    text = "* %s  %s  %s: %s\n" % (Type, Time, IFName, text)
    #print type(text)
    simpletools.fopen(os.path.join(common.RSettings('dir_db'),'history.txt'), 'ab', bytearray(text, 'utf-8'))

class API():
  # настройки задаются один раз. Но можно написать модуль для изменения
  # настроек через канал общения.
  settings = {'history': True,
              'monitor': True, # включает вывод на экран статистику работы ИСУ
              'logic': True, # включает модуль логики
              'convert2IL': True, # включает последний этап конвертации
                               # если при отключении включёна логика, то будет ошибка
              'language': 'Esperanto',
              'storage_version': 2,
              'assoc_version': 1,
              'test': True, # тестовый режим, включаемый в процессе отладки и разработки
              'dir_db': None
  }
  # настройки для модулей интерфейсов
  # 'module_settings': {ИмяМодуля: СловарьНастроекМодуля_ИлиОбъектУправления}
  def ChangeSettings(self, NewSettings):
    # Проверяем правильность ключей
    keys = self.settings.keys()
    for user_key in NewSettings.keys():
      if user_key not in keys:
        raise MainException('error2: Wrong name of key in settings: %s' % str(user_key))
    # Обновляем настройки
    self.settings.update(NewSettings)
    self.settings['language'] = self.settings['language'].capitalize()

    if self.settings['dir_db'] == None: db_path = os.path.dirname(os.path.abspath(''))
    else: db_path = self.settings['dir_db']
    db_path = os.path.join(db_path, 'DATA_BASE')
    if not os.path.exists(db_path) or not os.path.isdir(db_path):
      os.mkdir(db_path)
    os.chdir(db_path)
    self.settings['dir_db'] = db_path

    common.WSettings(self.settings)
    #print db_path, sys.path

  def __init__(self, UserSettings={}):
    """ Инициализация ИСУ """
    # Меняем настройки по умолчанию на пользовательские
    self.ChangeSettings(UserSettings)
    print(u"Загрузка модулей действий...")
    t1 = time.time()
    Import = import_action.ImportAction(self.settings)
    Import.importAll()
    t2 = time.time()
    print'  ', t2 - t1
    print(u"Загрузка модуля естественного языка...")
    t1 = time.time()
    self.LangClass = LangClass(self.settings)
    t2 = time.time()
    print '  ', t2 - t1
    print(u"Инициализация модуля логики...")
    t1 = time.time()
    self.LogicShell = FCModule.LogicShell(self.settings)
    t2 = time.time()
    print '  ', t2 - t1
    print(u"Готово!")

  def print_errors(self, GrammarNazi, ErrorConvert):
    for analys, errors in GrammarNazi.items():
      if errors: sys.stderr.write(analys + ": ")
      for error in errors: sys.stderr.write("  " + error + "\n")
    for part, errors in ErrorConvert.items():
      if errors: sys.stderr.write(part + ":\n")
      for error in errors:
        if not error: continue
        if not (isinstance(error, str) or isinstance(error, unicode)): error = str(error)
        sys.stderr.write("  " + error + "\n")

  def toString(self, r_text):
    if not isinstance(r_text, unicode): return unicode(r_text)

  def write_text(self, IFName, w_text):
    #print 'write', type(w_text)
    if w_text:
      if self.settings['history']: _save_history(w_text, "W", IFName)
      _ILs, GrammarNazi, ErrorConvert = self.LangClass.NL2IL(w_text)
      self.print_errors(GrammarNazi, ErrorConvert)
      ExecError = self.LogicShell.execIL(_ILs, GrammarNazi, ErrorConvert, IFName)

  def read_text(self, IFName, index=None):
    if IFName not in self.LogicShell.list_answers: self.LogicShell.list_answers[IFName] = []
    # Возвращает ответ или пустую строку, если ответа нет. None ответом не считается.
    r_text = u''
    if index == None:
      r = range(len(self.LogicShell.list_answers[IFName]))
      # montru dolaran euxran cambion de ukraina banko
      for i in r:
        _r_text = self.LogicShell.list_answers[IFName].pop(0)
        r_text += self.toString(self.LangClass.IL2NL(_r_text)) + ' '
    else:
      if len(self.LogicShell.list_answers[IFName]) > 0:
        _r_text = self.LangClass.IL2NL(self.LogicShell.list_answers[IFName].pop(index))
        r_text = self.toString(_r_text)
    if self.settings['history']: _save_history(r_text, "R", IFName)
    return r_text

  def getlen_text(self, IFName):
    if IFName not in self.LogicShell.list_answers: self.LogicShell.list_answers[IFName] = []
    return len(self.LogicShell.list_answers[IFName])
