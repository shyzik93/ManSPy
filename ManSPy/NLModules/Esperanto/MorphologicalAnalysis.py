# -*- coding: utf-8 -*-
''' Модлуль выполняет стандартный морфологический анализ слова ЕЯ Эсперанто,
    основывваясь только на морфологических признаках (на внешнем виде слова)

    Оприсание словаря - результата разбора:
      Обязательные значения:
      res['word'] - данная форма слова
      res['base'] - корень слова
      res['POSpeech'] - часть речи
'''

import Dict
import re

#template = re.compile(r'[0-9]+(\.|\,)?[0-9]*')

combain_numerals_template = re.compile(('^(%s)('+Dict.dct['numeral'][-5]+'|'+Dict.dct['numeral'][-4]+')$') % '|'.join(Dict.dct['numeral'][:-5]))
mili_numerals_template = re.compile(('^(%s)(iliard|ilion)$') % '|'.join(Dict.dct['numeral'][:-5]))

def checkByDict(word_l, word):
  ''' Определяет часть речи по словарю
      для неизменяемых или почти неизменяемых частей речи'''
  for POSpeech, data in Dict.words.items():
    if word_l not in data: continue
    word.update(data[word_l])
    word['POSpeech'] = POSpeech
    word['base'] = word_l
    return True

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
  if not word['word'][0].islower():
    word['name'] = 'proper' # имя собственное
  else: word['name'] = 'common' # имя нарицательное

def isNumeral(word_l, word):
  if word_l in Dict.words['numeral']:
    word.update(Dict.words['numeral'][word_l])
    return True

  combain_numerals = combain_numerals_template.findall(word_l)
  if combain_numerals: combain_numerals = combain_numerals[0]
  mili_numerals = mili_numerals_template.findall(word_l)
  if mili_numerals: mili_numerals = mili_numerals[0]

  if combain_numerals:
    factor1, factor2 = combain_numerals
    number_value = int(Dict.dct['numeral_d'][factor1]) * int(Dict.dct['numeral_d'][factor2])
  elif mili_numerals:
    factor1, factor2 = mili_numerals
    number_value = int(Dict.dct['numeral_d'][factor1]) ** int(Dict.dct['numeral_d']['m'+factor2])
  else: return False

  word['number_value'] = number_value
  return True

def _getMorphA(word, GrammarNazi):

  word_l = word['word'].lower()

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

  #combain_numerals = combain_numerals_template.findall(word_l)
  #if combain_numerals: combain_numerals = combain_numerals[0]
  #mili_numerals = mili_numerals_template.findall(word_l)
  #if mili_numerals: mili_numerals = mili_numerals[0]
  #print combain_numerals, mili_numerals

  # существительное
  if ends[0] == 'o':
    defaultNoun(words[0], word)
    if isNumeral(words[0], word): word['derivative'] = 'numeral' # производное от числительного

  # наречие
  elif ends[0] == 'e':
    word['POSpeech'] = 'adverb'
    word['base'] = words[0]
    if isNumeral(words[0], word): word['derivative'] = 'numeral' # производное от числительного

  # прилагательное, притяжательное местоимение или порядковое числительное
  elif ends[0] == 'a':
    if checkByDict(words[0], word): # прилагательное
      if word['POSpeech'] == 'pronoun': # притяжательное иестоимение
        word['category'] = 'possessive'
      elif word['POSpeech'] == 'numeral': # порядковое числительное
        word['class'] = 'ordinal'
      else: # прилагательное (есть ли такие: dea, laa, kaja и подобные?)
        word['POSpeech'] = 'adjective'
        word['case'] = 'nominative'
        word['number'] = 'singular'
        word['base'] = words[0]
    elif isNumeral(words[0], word): # порядковое числительное
      word['POSpeech'] = 'numeral'
      word['class'] = 'ordinal'
      word['base'] = words[0]
    else:
      word['POSpeech'] = 'adjective'
      word['case'] = 'nominative'
      word['number'] = 'singular'
      word['base'] = words[0]

  # глагол
  elif ends[0] in Dict.dct['verb']['end'].keys() or ends[1] in Dict.dct['verb']['end'].keys():
    word['POSpeech'] = 'verb'
    for i in range(2):
      if ends[i] not in Dict.dct['verb']['end']: continue
      word.update(Dict.dct['verb']['end'][ends[i]])
      if isNumeral(words[i], word): word['derivative'] = 'numeral' # производное от числительного
      word['base'] = words[i]
      break

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
  elif isNumeral(word_l, word):#combain_numerals:#len_word >= 5:
    #factor1, factor2 = combain_numerals
    word['POSpeech'] = 'numeral'
    word['word'] = word_l
    word['base'] = word_l
    word['class'] = 'cardinal' # количественное
    #word['number_value'] = int(Dict.dct['numeral_d'][factor1]) * int(Dict.dct['numeral_d'][factor2])

  # число (считается как числительное)
  elif word['notword'] == 'figure':#re.match(r'[0-9]+(\.|\,)?[0-9]*', word_l):
    word['POSpeech'] = 'numeral'
    word['class'] = 'cardinal'
    word['word'] = word_l
    word['base'] = word_l
    word['number_value'] = float(word_l.replace(',', '.'))

  # анализ приставок
  if 'base' in word:
    base = word['base']
    if len(base) > 3 and base[:3] in Dict.dct['prefix']:
      word['antonym'] = Dict.dct['prefix'][base[:3]]['antonym']
      word['base'] = base[3:]

  if len(word) == 1: # то есть {'word': word}
    # нераспознанное слово с большой буквы - существительное
    if word['word'][0].islower() == False:
      defaultNoun(word_l, word)
    else: word['POSpeech'] = ''

def getMorphA(sentences, GrammarNazi):
  ''' Обёртка '''
  for index, sentence in sentences:
    for index, word in sentence:
      _getMorphA(word, GrammarNazi)
  return sentences

#sentence = 'vi montru kursojn de mia dolaro'
#sentence = '1444 123.78654 345,976 0.7 9,8'
#sentence = 'triA unu Tridek kvarcent du mil'
