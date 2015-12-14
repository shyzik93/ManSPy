# -*- coding:utf-8 -*-
import pickle, copy, time, json, re
from pprint import pprint
import common

string = None

def iseq(pattern):
  global string
  #print len(pattern), len(string)
  #print 'pattern:', pattern, '\nstring:',  string
  res = re.findall(pattern, string)
  return 1 if res else 0

class FasifDB():
  def __init__(self, settings):
    self.settings = settings
    self.c, self.cu = common.create_bd_file(settings['language'], 'main_data.db')
    self.c.create_function('iseq', 1, iseq)
    self.cu.executescript('''
      -- CREATE TABLE IF NOT EXISTS dicts (
      --   dict TEXT COLLATE NOCASE UNIQUE ON CONFLICT IGNORE,
      --   id_dict INTEGER PRIMARY KEY);
      CREATE TABLE IF NOT EXISTS fasifsWComb (
        pattern TEXT UNIQUE ON CONFLICT IGNORE,
        dict TEXT,
        argdescr TEXT,
        wcomb_func TEXT);
      CREATE TABLE IF NOT EXISTS fasifsVerbs (
        verb TEXT,
        verb_func TEXT); ''')

  #def add_dict(self, _dict):
  #  self.cu.execute('INSERT INTO dicts (dict) VALUES (?)', (json.dumps(_dict, sort_keys=True),))
  #  self.c.commit()

  def add_hashWComb(self, pattern, _dict, argdescr, wcomb_func):
    self.cu.execute('INSERT INTO fasifsWComb (pattern, dict, argdescr, wcomb_func) VALUES (?,?,?,?)',
                    (pattern, json.dumps(_dict, sort_keys=True), argdescr, wcomb_func))
    self.c.commit()

  def get_hashWComb(self, _string):
    global string
    string = _string
    res = self.cu.execute('SELECT dict, argdescr, wcomb_func FROM fasifsWComb WHERE iseq(pattern)=1').fetchall()
    return res[0] if res else None

  def add_hashVerb(self, verb, verb_func):
    self.cu.execute('INSERT INTO fasifsVerbs (verb, verb_func) VALUES (?,?,?,?,?,?)',
                    (verb, verb_func))
    self.c.commit()

  def get_hashVerb(self, verb):
    res = self.cu.execute('SELECT verb_func FROM fasifsVerbs WHERE verb=?',
                    (verb,)).fetchall()
    return res[0][0] if res else None

def return_features(dict_wcomb):
  _dict_wcomb = {}
  _index = 0
  for index, dword in dict_wcomb.items():
    for feature in dword['feature']:
      _dict_wcomb[_index] = feature
      del feature['feature']
      _index += 1
    _dict_wcomb[_index] = dword
    del dword['feature']
    _index += 1
  return _dict_wcomb

'''def copy_word(dict_word, *usefull_properties):
  _dict_word = {}
  for _property, value in dict_word.items(): # падежей и фичей не должно быть! Падежи удаляются из фичей в постморфологическом анализе.
    if _property not in usefull_properties: continue
    _dict_word[_property] = value
    if _property == 'feature':
      for index, feature in enumerate(value): _dict_word[_property][index] = copy_word(feature, *usefull_properties)
  return _dict_word'''

def copy_word(dict_word, *usefull_properties):
  _dict_word = {}
  for _property in usefull_properties: # падежей и фичей не должно быть! Падежи удаляются из фичей в постморфологическом анализе.
    if _property not in dict_word: continue
    _dict_word[_property] = dict_word[_property]
  return _dict_word

def word2formule(dword):
  keys = dword.keys() # для сортировки словаря
  keys.sort()

  fword = []
  for key in keys:
    value = dword[key]
    fword.append(key+u':'+value)
  return ','.join(fword)

ANY_DEFINITION = r'POSpeech:adjective,base:'

def wcomb2formule(dict_wcomb, isreg):
  keys = dict_wcomb.keys() # для сортировки словаря # ля Питон3 - list(dict_wcomb.keys())
  keys.sort()

  fwcomb = []
  for key in keys:
    dword = dict_wcomb[key]
    if isreg:
      fwcomb.append('(?:'+word2formule(dword)+';)')
    else: fwcomb.append(word2formule(dword)+';')
  #print fwcomb
  return ''.join(fwcomb)

def to_formule(_dict_wcomb, isreg=True, _args=None): # третий аргумент передаём, если второй = True
  # возвращаем определения и обстоятельства из свойств слова в предложение
  _dict_wcomb = return_features(_dict_wcomb)
  # копируем словосочетание с нужными свойствами слов
  '''_min = min(_dict_wcomb.keys())
  _dict_wcomb[_min] = copy_word(_dict_wcomb[_min], 'POSpeech', 'base', 'feature') # падеж и член предложения первого чдена не учитывается (они могут иметь разные падежи членства)
  for index, _dict_word in _dict_wcomb.items()[1:]:
    _dict_wcomb[index] = copy_word(_dict_word, 'POSpeech', 'base', 'case', 'feature')'''
  first = True
  for index, _dict_word in _dict_wcomb.items():
    if _dict_word['MOSentence'] in ['definition', 'circumstance']: _dict_wcomb[index] = copy_word(_dict_word, 'MOSentence', 'base')
    elif first == True and _dict_word['MOSentence'] in ['direct supplement', 'supplement', 'subject']:
      _dict_wcomb[index] = copy_word(_dict_word, 'POSpeech', 'base')
      first = False
    elif first == False and _dict_word['MOSentence'] in ['direct supplement', 'supplement', 'subject']: _dict_wcomb[index] = copy_word(_dict_word, 'MOSentence', 'base', 'case')
  #pprint(_dict_wcomb)

  if isreg:
    args = {}
    for argname, data in _args.items():
      dword = data['argwords']['in_wcomb']['name']
      dword['isreq'] = data['isreq']
      args[dword['base']] = dword

    dict_wcomb = {}
    index = 0
    for _index, dword in _dict_wcomb.items():
      if dword['base'] in args:
        #if 'case' in keys and dword['case'] != args[value]['case']: continue # если есть падеж, то учитываем его
        dword['base'] = ur'[a-zа-яёĉĝĥĵŝŭ]+'
      dict_wcomb[index] = dword
      index += 1

  else:
    args = None
    dict_wcomb = _dict_wcomb

  # составляем регулярное выражение
  fwcomb = wcomb2formule(dict_wcomb, isreg)
  return r'^'+fwcomb+'$' if isreg else fwcomb

######### Получение хеша словосочетания

'''def copy_word(dct_word, absent=[]):
  _dct_word = {}
  for characteristic, value in dct_word.items():
    if characteristic not in ['MOSentence', 'POSpeech', 'case', 'feature', 'base']: continue
    if characteristic in absent: continue # absent - те характеристики, которые должны исключится из списка нужных
    if characteristic == 'feature':
      value = copy.deepcopy(value)
      for fea_index, fea_word in enumerate(value):
        value[fea_index] = copy_word(fea_word, ['case', 'POSpeech'])
    _dct_word[characteristic] = value
  return _dct_word

def to_hash(dct_sentence):
  dct_sentence = word_combination.getUnit('dict', 'members', 'info')
  _dct_sentence = {}
  # падеж и член предложения первого чдена не учитывается (они могут иметь разные падежи членства)
  _dct_sentence[0] = copy_word(dct_sentence[0], ['case', 'MOSentence'])

  for index, dct_word in dct_sentence.items()[1:]:
    _dct_sentence[index] = copy_word(dct_word)
  #pprint(_dct_sentence, indent=4)
  json_sentence = json.dumps(_dct_sentence,  sort_keys=True)
  return hash(json_sentence), json_sentence'''
'''
-1965140811
2003176567
-1965140811
'''
'''if __name__ == '__main__':
  import analyse_text
  settings = {'history': 1,
              'monitor': 1, # включает вывод на экран статистику работы ИСУ
              'logic': 1, # включает модуль логики
              'convert2IL': 1, # включает последний этап конвертации
                               # если при отключении включёна логика, то будет ошибка
              'language': 'Esperanto',
              'storage_version': 2,
              'converter_version': 1,
              'test': True, # тестовый режим, включаемый в процессе отладки и разработки
              'dir_db': None
  }
  LC = analyse_text.LangClass(settings)

  word_combinations = [
    "dolara cambio de rusia kaj ukrainia banko",
    "dolara cambio de rusia banko",
    "dolaran cambion de rusia kaj ukrainia banko"]
  db = {}
  for _word_combination in word_combinations:
    word_combination = LC.NL2IL(_word_combination, ":synt")[0][0]
    #pprint(word_combination.getSentence('dict'), indent=4)
    wc_hash = to_hash(word_combination.getUnit('dict', 'members', 'info'))[0]
    print wc_hash, _word_combination
    db[wc_hash] = [_word_combination, word_combination]
  print db
'''
