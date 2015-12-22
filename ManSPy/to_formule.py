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

def compare_word(word, position, worddescr):
  #print word['base'], worddescr['base'], worddescr['type']
  if word['MOSentence'] not in ['direct supplement', 'supplement', 'subject'] or \
     worddescr['POSpeech'] != word['POSpeech'] or \
     not (position == 0 or worddescr['case'] == word['case']): return False
  #print word['base'], worddescr['base'], 'argname' not in worddescr
  if 'argname' not in worddescr: # если константное слово
    if worddescr['base'] != word['base']: return False
    return True
  else:
    # проверяем вхождение корня в гиперонимы из описания
    return True

def compare_fasif_WordCombination(fasif, argument):
  functions = fasif['functions']
  _argument = NLModules.ObjUnit.Sentence(fasif['wcomb'])
  _argument_iter = NLModules.ObjUnit.Sentence(fasif['wcomb']).__iter__()

  '''_index = 0
  prev_index = None
  for index, word in argument.itemsUnit():
    controls = argument.getControl(index)
    if prev_index != None and (not controls or controls[0] != prev_index): continue
    isright = compare_word(word, _index, _argument)
    if not isright:
      if word['homogeneous_link']: pass # обработать так, как будто это продолжение актанта
      else: return False
    _argument.next()
    prev_index = index
    _index += 1'''

  #for i in argument: print i

  for index, word in argument:
    try: isright = compare_word(word, argument.position, _argument_iter.next()[1])
    except StopIteration: break
    if not isright: return False
    indexes = argument.getObient(index)
    if indexes:
      argument.jumpByIndex(indexes[0])
      argument.jump(-1)
    else: break

  return True

argument = None
def iseq(_type, fasif):
  global argument
  #print 'fasif:', fasif, '\nargument:',  argument
  fasif = json.loads(fasif)
  if _type == 'WordCombination': isright = compare_fasif_WordCombination(fasif, argument)
  return 1 if isright else 0

class FasifDB():
  def __init__(self, settings):
    self.settings = settings
    self.c, self.cu = common.create_bd_file(settings['language'], 'main_data.db')
    self.c.create_function('iseq', 2, iseq)
    self.cu.execute('''
      CREATE TABLE IF NOT EXISTS fasifs (
        _type TEXT,
        fasif TEXT); ''')

  def safeFASIF(self, _type, fasif):
    self.cu.execute('INSERT INTO fasifs (_type, fasif) VALUES (?,?)',
                    (_type, json.dumps(fasif, sort_keys=True)))
    self.c.commit()

  def getFASIF(self, _type, _argument):
    global argument
    argument = _argument
    res = self.cu.execute('SELECT fasif FROM fasifs WHERE _type=? AND iseq(_type, fasif)=1', (_type,)).fetchall()
    return res[0] if res else None
