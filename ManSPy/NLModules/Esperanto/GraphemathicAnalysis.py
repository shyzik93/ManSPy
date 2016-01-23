# -*- coding: utf-8 -*-
""" Графематический анализ текста.
    Словарь символа: {'symbol': Символ, 'type': 'letter' OR 'punctuation_mark' OR 'other'}
    Словарь слова: {'word': СписокСимволов}
    Задача модуля: выдать предложение, состоящее из слов и неслов. Неслова - это текст в кавычках, имена файлов, адреса и прочее, что может испортить последущие анализы.
    Благодаря чему морфологический модуль будет уже знать, где слово, а где - не слово..
"""
import re

low_letters = u"ABCĈDEFGĜHĤIJĴKLMNOPRSŜTUŬVZ"
up_letters =  u"abcĉdefgĝhĥijĵklmnoprsŝtuŭvz"
letters = up_letters + low_letters
punctuation_marks = u".,;:!?-'\""

ReplacedLetters = {u'cx' :u'ĉ', u'gx': u'ĝ', u'hx': u'ĥ',
           u'jx': u'ĵ', u'sx': u'ŝ', u'ux': u'ŭ',
           u'\t': u'', u'\n': u''}

def define_type_symbol(word):
  l = len(word)
  for symbol in range(l):
    symbol = word(symbol)
    if symbol['symbol'] in letters: symbol['type'] = 'letter'
    elif symbol['symbol'] in punctuation_marks: symbol['type'] = 'pmark'
    else: symbol['type'] = 'other'

def proccessEndWord(sword, word, symbols):
  for index in range(1, len(sword)):
    if sword[-index] not in symbols: break
    word['end_orig'] += sword[-index]
  word['word'] = sword[:-len(word['end_orig'])]

def getGraphmathA(text, ObjUnit):
  # Заменяем символы
  for k, v in ReplacedLetters.items(): text = text.replace(k, v)
  words = text.split()
  words = [ObjUnit.Word(word) for word in words]

  for word in words: define_type_symbol(word)

  # Присоединяем отдельностоящие символы пунктуации к концу слова
  index = 0
  while index < len(words):
    word = words[index]
    sword = word['word']
    if re.match(r'(?:[.]+)|(?:[,]+)|(?:[?!]+)|(?:[:]+)', sword):
      if index: words[index-1]['word'] += sword
      del words[index]
      index -= 1
    index += 1

  # Обработка последних символов в слове (потенциальные пунктуационные знаки)
  for word in words:
    sword = word['word']
    word['end'] = word['end_orig'] = ''
    # слово с пунктуационными символами на конце
    if sword[-1] in '.!?':
      proccessEndWord(sword, word, '.!?')
      if '?' in word['end_orig']: word['end'] = '?'
      elif '!' in word['end_orig']: word['end'] = '!'
      elif '...' in word['end_orig']: word['end'] = '...'
      elif '.' in word['end_orig']: word['end'] = '.'
    elif sword[-1] in ',;:':
      proccessEndWord(sword, word, ',;:')
      word['end'] = word['end_orig'][0]
    # слово с небуквенными символами в середине или начале
    if not word['word'].isalpha():
      if re.match(r'^[0-9]*[,.]?[0-9]+$', sword): word['notword'] = 'figure'

  # обработка кавычек вокруг одного слова
  for word in words:
    sword = word['word']
    if sword[-1] == sword[0] and (sword[-1] == '"' or sword[-1] == "'"):
      word['word'] = sword[1:-1]
      word['around_pmark'].append('quota')

  # Разбиваем текст на ВОЗМОЖНЫЕ предложения
  sentences = []
  sentence = ObjUnit.Sentence({})
  for word in words:
    sentence.append(word)
    if word['end'] in ['.', '...', '!', '?']:
      sentences.append(sentence)
      sentence = ObjUnit.Sentence({})
  if len(sentence) > 0:
    sentences.append(sentence)
    sentence['end'] = '.'

  #print len(words), len(sentences)
  #for sentence in sentences:
  #  print len(sentence)#sentence.getUnit('dict')


  # обработка кавычек

  # обработка слов, с небуквенными символами (email, url, file, etc)

  return ObjUnit.Text(sentences)
