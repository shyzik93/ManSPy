# -*- coding: utf-8 -*-
import pickle, os, sqlite3 as sql

settings_path = os.path.join(os.path.dirname(__file__), 'settings.pckl')

''' Функции-обёртки для удобства '''
def _toDump(path, data):
  with open(path, 'w') as f: pickle.dump(data, f)
def _fromDump(path):
  with open(path, 'r') as f: data = pickle.load(f)
  return data

''' Консервирует настройки '''
def WSettings(settings): _toDump(settings_path, settings)
''' Возвращает настройки '''
def RSettings(*keys):
  settings = _fromDump(settings_path)
  if not keys: return settings
  else:
    res = [settings[key] for key in keys]
    return res if len(res) > 1 else res[0]

def create_bd_file(language, name):
  db_dir = RSettings('dir_db')
  if not os.path.exists(db_dir) or not os.path.isdir(db_dir):
    os.mkdir(db_dir)
  db_dir = os.path.join(db_dir, language)
  if not os.path.exists(db_dir) or not os.path.isdir(db_dir):
    os.mkdir(db_dir)
  name = os.path.join(db_dir, name)
  c = sql.connect(name)
  cu = c.cursor()
  return c, cu


#WriteSettings({'hi': 9, 0: 6, 'pickle': 'smickle'})
#print GetSettings('hi')
#print GetSettings('hi', 0)
