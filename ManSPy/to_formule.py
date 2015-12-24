# -*- coding:utf-8 -*-
'''
Созранение:
1. Парсится ФАСИФ.
2. В БД сохраняется ФАСИФ и его тип.

Конвертация:
1. Предложение декомпозируется на сказуемое (предикат) и его актанты. Среди актантов могут быть однородные актанты.
2. Для каждого актанта определяется ФАСИФ WCombination-типа.
3. Выделяем аргументные слова из актанта и строим словарь аргументов.
4. Если в предложении употреблён общий глагол, то аргументы передаются в функцию запроса статуса, а результат - в функцию общего глагола.
   Иначе, аргументы подаются в функцию употреблённого глагола.

Определение ФАСИФа определяется через проверку соответветсвия актанта актанту, указанного в ФАСИФе. Алгоритм проверки соответствия:
1. Проверяется каждое словосочетание актанта:
  1. Если дополнение - это константа, то производим точное сравенение с первым дополнение актанта в ФАСИФе.
     Иначе - точная проверка кроме корня. Корень проверяем на вхождение в требуемые гиперонимы.
  2. Для определений - так же.

На четвёртом шаге перед выполнением функций необходио сформировать внутренний язык. Функции выполнятся в модуле логики.

'''

import copy, time, json
from pprint import pprint
import common, NLModules

def compare_word(word, position, argworddescr, finded_args):
  #print word['base'], worddescr['base'], worddescr['type']
  if word['MOSentence'] in ['direct supplement', 'supplement', 'subject']:
     if argworddescr['POSpeech'] != word['POSpeech'] or \
        not (position == 0 or argworddescr['case'] == word['case']): return False # для первого дополнения падеж не учитывается
  elif word['MOSentence'] in ['definition', 'circumstance']:
     if argworddescr['POSpeech'] != word['POSpeech']: return False # для первого дополнения падеж не учитывается
  else: return False
  #print word['base'], worddescr['base'], 'argname' not in worddescr
  if 'argname' not in argworddescr: # если константное слово
    if argworddescr['base'] == word['base']: return True
    return False
  else:
    if argworddescr['argname'] not in finded_args: finded_args[argworddescr['argname']] = []
    finded_args[argworddescr['argname']].append(word['base'])
    # проверяем вхождение корня в гиперонимы из описания
    return True

def compare_fasif_WordCombination(fasif, argument, finded_args):
  functions = fasif['functions']
  _argument = NLModules.ObjUnit.Sentence(fasif['wcomb'])
  _argument_iter = NLModules.ObjUnit.Sentence(fasif['wcomb']).__iter__()

  for index, word in argument:
    _index, _word = _argument_iter.next() # new

    # "Проходимся" по дополнениям (прямые, косвенные, а также подлежащие)
    isright = compare_word(word, argument.position, _word, finded_args) # new
    #try: isright = compare_word(word, argument.position, _argument_iter.next()[1]) # old
    #except StopIteration: break # игнорируем лишние косвенные дополнения (на хвосте) #old
    #if not isright and 'argname' not in _word: return False # если отсутствует контсантное слово - актант не соответсвует фасифу
    if not isright: return False # если посреди свезей чужой член - актант не соответсвует фасифу
    indexes = argument.getObient(index)
    if indexes:
      argument.jumpByIndex(indexes[0])
      argument.jumpByStep(-1)
    #else: break
    _indexes = _argument.getObient(_index) # new
    if _indexes: # new
      _argument.jumpByIndex(_indexes[0]) # new
      _argument.jumpByStep(-1) # new
    #else: break # new

    # "Проходимся" по обстоятельствам и определениям
    features = word['feature']
    _features = _word['feature']
    for feature in features:
      for _feature in _features:
        isright = compare_word(feature, argument.position, _feature, finded_args)
        # не проверяем на верность.

    # "Проходимся" по однородным дополнениям (прямые, косвенные, а также подлежащие), если это не первый член

    # игнорируем лишние косвенные дополнения (на хвосте)
    if not (indexes and _indexes): break

  return True

'''argument = None
def iseq(_type, fasif):
  global argument
  #print 'fasif:', fasif, '\nargument:',  argument
  fasif = json.loads(fasif)
  if _type == 'WordCombination': isright = compare_fasif_WordCombination(fasif, argument)
  return 1 if isright else 0'''

class FasifDB():
  def iseq(self, id_fasif, type_fasif, fasif):
    #print 'fasif:', fasif, '\nargument:',  argument
    fasif = json.loads(fasif)
    finded_args = {}
    if type_fasif == 'WordCombination': isright = compare_fasif_WordCombination(fasif, self.argument, finded_args)
    if isright: self.compared_fasifs[id_fasif] = (finded_args, fasif)
    return 1 if isright else 0

  def __init__(self, settings):
    self.settings = settings
    self.c, self.cu = common.create_bd_file(settings['language'], 'main_data.db')
    self.c.create_function('iseq', 3, self.iseq)
    self.cu.execute('''
      CREATE TABLE IF NOT EXISTS fasifs (
        id_fasif INTEGER PRIMARY KEY AUTOINCREMENT,
        type_fasif TEXT,
        fasif TEXT UNIQUE ON CONFLICT IGNORE); ''')

  def safeFASIF(self, _type, fasif):
    self.cu.execute('INSERT INTO fasifs (type_fasif, fasif) VALUES (?,?)',
                    (_type, json.dumps(fasif, sort_keys=True)))
    self.c.commit()

  def getFASIF(self, _type, argument):
    self.argument = argument
    self.compared_fasifs = {}
    res = self.cu.execute('SELECT id_fasif FROM fasifs WHERE type_fasif=? AND iseq(id_fasif, type_fasif, fasif)=1', (_type,)).fetchall()
    return self.compared_fasifs
