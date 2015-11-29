# -*- coding: utf-8 -*-
''' Модлуль выполняет стандартный морфологический анализ слова ЕЯ Эсперанто,
    основывваясь только на морфологических признаках (на внешнем виде слова)

    Оприсание словаря - результата разбора:
      Обязательные значения:
      res['word'] - данная форма слова
      res['base'] - корень слова
      res['POSpeech'] - часть речи
'''

from Esperanto_Dict import dct
import re

template = re.compile(r'[0-9]+(\.|\,)?[0-9]*')

def checkByDict(word_l, word):
  ''' Определяет часть речи по словарю
      для неизменяемых или почти неизменяемых частей речи'''
  global dct
  if word_l in dct['article']: word['POSpeech'] = 'article'             # артикль
  elif word_l in dct['particle']: word['POSpeech'] = 'particle'         # частица
  elif word_l in dct['conjunction']:
    word['POSpeech'] = 'conjunction'      # союз
    if word_l in dct['conjunction_d']['coordinating']: word['value'] = 'coordinating'
    elif word_l in dct['conjunction_d']['subordinating']: word['value'] = 'subordinating'
                         # непроизводное наречие (не всегда имеет окончание -e)
  elif word_l in dct['adverb']['non-derivative']: word['POSpeech'] = 'adverb'
  elif word_l in dct['preposition']:                                   # предлог
    word['POSpeech'] = 'preposition'
    word['give_case'] = dct['preposition_d'][word_l]
  elif word_l in dct['pronoun']:                                    # местоимение
    word['POSpeech'] = 'pronoun'
    word['case'] = 'nominative' # именительный
    word['category'] = 'personal'
  elif word_l in dct['numeral']:                                    # числительное
    word['POSpeech'] = 'numeral'
    word['figure'] = dct['numeral_d'][word_l]
    word['class'] = 'cardinal' # количественное
  else: return 0 # часть речи не определена
  word['base'] = word_l
  return 1

def getNumberAndCase(word_l):
  '''возвращает число, падеж и начальную форму
     (функция для прилагательного, существительного или местоимения)'''
  temp_word = {'case': 'nominative',
         'number': 'singular' }
  if word_l[-1] == 'n':
    word_l = word_l[:-1]
    temp_word['case'] = 'accusative'
  if word_l[-1] == 'j':
    word_l = word_l[:-1]
    temp_word['number'] = 'plural'
  temp_word['base'] = word_l
  return temp_word

def defaultNoun(word_l, word):
  ''' Устанавливает параметры по умолчанию
      На вход подаётся слово без окончания'''
  word['POSpeech'] = 'noun'
  word['base'] = word_l
  word['case'] = 'nominative' # именительный
  word['number'] = 'singular'
  # определение по первой букве:
  if word['word'][0].islower() == False:
    word['name'] = 'proper' # имя собственное
  else: word['name'] = 'common' # имя нарицательное

def _getMorphA(word, GrammarNazi):

  word_l = word['word'].lower()
  if word_l[-1] in '\'".,:!?)': word_l = word_l[:-1]
  if word_l[0] in '(': word_l = word_l[0:]

  # Определение части речи по словарю
  # (для неизменяемых или почти неизменяемых частей речи)
  if checkByDict(word_l, word): return

  # Определение части речи по окончанию
  len_word = len(word_l)
  ends = ['', ''] # окончания двух возможных длин
  words = ['', ''] # корни, в зависимости от окончания
  if len_word >= 2:
    ends[0] = word_l[-1]
    words[0] = word_l[:-1]
  if len_word >= 3:
    ends[1] = word_l[-2:]
    words[1] = word_l[:-2]

  # существительное
  if ends[0] == 'o':
    defaultNoun(words[0], word)

  # наречие
  elif ends[0] == 'e':
    word['POSpeech'] = 'adverb'
    word['base'] = words[0]

  # прилагательное, притяжательное местоимение или порядковое числительное
  elif ends[0] == 'a':
    _res = checkByDict(words[0], word)
    if _res == 0: # прилагательное
      word['POSpeech'] = 'adjective'
      word['case'] = 'nominative'
      word['number'] = 'singular'
      word['base'] = words[0]
    elif word['POSpeech'] == 'pronoun': # притяжательное иестоимение
      #word.update(_res)
      word['category'] = 'possessive'
    elif word['POSpeech'] == 'numeral': # порядковое числительное
      word['class'] = 'ordinal'
      del word['case']
    else: # прилагательное (есть ли такие: dea, laa, kaja и подобные?)
      word['POSpeech'] = 'adjective'
      word['case'] = 'nominative'
      word['number'] = 'singular'
      word['base'] = words[0]

  # глагол
  elif ends[0] in dct['verb']['end'].keys() or ends[1] in dct['verb']['end'].keys():
    word['POSpeech'] = 'verb'
    for i in range(2):
      if ends[i] in dct['verb']['end']:
        word.update(dct['verb']['end'][ends[i]])
        word['base'] = words[i]

  # мн. ч. существительно, прилагательного, притяжательно местоимения. И вин. падеж прилагательного, существительного, местоимения или притяхательного местоимения.
  #ERROR слово prezenten и enden определяется наречием. Другие слова на -n могут ошибочно определиться.
  elif ends[0] in ['j', 'n'] or ends[1] == 'jn':
    temp_word1 = getNumberAndCase(word_l)
    temp_word2 = {'word': temp_word1['base']}
    _getMorphA(temp_word2, GrammarNazi)
    word.update(temp_word2)
    word.update(temp_word1)
    word['word'] = word_l
    word['base'] = temp_word2['base']

  # сложное числительное (не составные!)
  elif len_word >= 5:
    parts = ['', ''] # разбитое на простые числительные
    for i in [2, 3, 4]:
      if word_l[:-i] in dct['numeral'][1:11]:
        parts[0] = word_l[:-i]
    for i in [3, 4]:
      if word_l[-i:] in dct['numeral'][10:12]:
        parts[1] = word_l[-i:]
    if '' not in parts:
      word['POSpeech'] = 'numeral'
      word['word'] = word_l
      word['base'] = word_l
      word['class'] = 'cardinal' # количественное
      word['figure'] = int(dct['numeral_d'][parts[0]]) * int(dct['numeral_d'][parts[1]])
    else: pass # значит, это что-то другое...

  # число (считается как числительное)
  elif re.match(template, word_l):
    word['POSpeech'] = 'numeral'
    word['word'] = word_l
    word['base'] = word_l
    word['figure'] = float(word_l.replace(',', '.'))

  # анализ приставок
  if 'base' in word:
    base = word['base']
    if len(base) > 3 and base[:3] in dct['prefix']:
      word['antonym'] = dct['prefix'][base[:3]]['antonym']
      word['base'] = base[3:]

  if len(word) == 1: # то есть {'word': word}
    # нераспознанное слово с большой буквы - существительное
    if word['word'][0].islower() == False:
      defaultNoun(word_l, word)
    else: word['POSpeech'] = ''

def getMorphA(sentences, GrammarNazi):
  ''' Обёртка '''
  for sentence in sentences:
    for word in sentence.getUnit('listSubUnits'):
      _getMorphA(word, GrammarNazi)
  return sentences

#sentence = 'vi montru kursojn de mia dolaro'
#sentence = '1444 123.78654 345,976 0.7 9,8'
#sentence = 'triA unu Tridek kvarcent du mil'
