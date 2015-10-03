# -*- coding: utf-8 -*-
import pickle, os, codecs

#DBPath = os.path.dirname(__file__) + '\\DATA_BASE\\' # доступна другим модулям
DBPath = os.path.abspath("DATA_BASE") # доступна другим модулям
settings_path = os.path.join(DBPath, "settings.pckl_")

# Функции-обёртки для удобства
def _toDump(path, data):
  f = open(path, 'w')
  pickle.dump(data, f)
  f.close()
def _fromDump(path):
  f = open(path, 'r')
  data = pickle.load(f)
  f.close()
  return data
  
# Консервирует настройки
def WriteSettings(Settings):
  global settings_path
  _toDump(settings_path, Settings)

# Возвращает настройки
def GetSettings(*keys):
  global settings_path
  settings = _fromDump(settings_path)
  if len(keys)==0: return settings
  else:
    RetSettings = []
    for key in keys:
      RetSettings.append(settings[key])
    if len(RetSettings) == 1: return RetSettings[0]
    else: return tuple(RetSettings)

# Консервирует словарь
def WriteOther(dataDict, name):
  global DBPath
  _toDump(os.path.join(DBPath, name+'.pckl'), dataDict)

# Возвращает словарь
def GetOther(name):
  global DBPath
  dataDict = _fromDump(os.path.join(DBPath, name+'.pckl'))
  return dataDict

# Сохраняет текстовые данные в файл
def WriteToFile(text, name, mode='w'):
  global DBPath
  name = os.path.join(DBPath, name + '.txt')

  if mode == 'a':
    if os.path.exists(name) == 0:
      f = open(name, 'w')
      f.close()
  
  with codecs.open(name, mode, 'utf-8') as f:
    f.write(text)
    f.close()
