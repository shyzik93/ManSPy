# -*- coding: utf-8 -*-
""" Графематический анализ текста.
    Словарь символа: {'symbol': Символ, 'type': 'letter' OR 'punctuation_mark' OR 'other'}
    Словарь слова: {'word': СписокСимволов}
"""
import re

low_letters = u"ABCĈDEFGĜHĤIJĴKLMNOPRSŜTUŬVZ"
up_letters =  u"abcĉdefgĝhĥijĵklmnoprsŝtuŭvz"
letters = up_letters + low_letters
punctuation_marks = u".,;:!?-'\""
end_of_sentence = '.!?'

ReplacedLetters = {u'cx' :u'ĉ', u'gx': u'ĝ', u'hx': u'ĥ',
           u'jx': u'ĵ', u'sx': u'ŝ', u'ux': u'ŭ',
           u'\t': u'', u'\n': u''}

def proccessEndSymbol(sword, word):
  for index in range(1, len(sword)):
    if sword[-index] not in end_of_sentence: continue
    

def define_type_symbol(word):
  l = len(word)
  for symbol in range(l):
    symbol = word(symbol)
    if symbol['symbol'] in letters: symbol['type'] = 'letter'
    elif symbol['symbol'] in punctuation_marks: symbol['type'] = 'pmark'

def getGraphmathA(text, ObjUnit):
  # Заменяем символы
  for k, v in ReplacedLetters.items(): text = text.replace(k, v)
  words = text.split()
  words = [ObjUnit.Word(word) for word in words]

  for word in words:
    define_type_symbol(word)

  # Разбиваем текст на ВОЗМОЖНЫЕ предложения, то есть это необходимо корректировать в следующих анализах
  '''sentences = []
  sentence = []
  for index, word in enumerate(words):
    sentence.append(word)
    sword = word['word']
    if sword.isalnum(): continue
    if sword[-1] in end_of_sentence:
      proccessEndSymbol(sword, word)
      sentences.append(sentence)
      sentence = []
    if re.findall('^['+end_of_sentence+']+$', sword): #если символы отдельно от слова (пробелом)
      del sentence[-1]
    
  # обработка запятой, точки с запятой, двоеточия
  for sentence in sentences:
    for index, word in enumerate(sentence):
       sword = word['word']

  # обработка кавычек

  # обработка слов, с небуквенными символами (email, url, file, etc)
'''

  # Разбиваем текст на ВОЗМОЖНЫЕ предложения, то есть это необходимо корректировать в следующих анализах
  sentences = [[]]
  index = 0
  for word in words:
    str_word = word['word']
    end_symbol = str_word[-1]
    sentences[index].append(word)    
    if end_symbol in '.!?':
      sentences.append([])
      index += 1
      word['symbol_map'][end_symbol] = str_word.index(end_symbol) # эту строку нужно сделать нормально: точек может быть несколько в слове (то есть список), определение индкса должно быть иначе
      word['word'] = str_word[:-1]
    if end_symbol in ',':
      word['symbol_map'][end_symbol] = str_word.index(end_symbol) # эту строку нужно сделать нормально: точек может быть несколько в слове (то есть список), определение индкса должно быть иначе
      word['word'] = str_word[:-1]
  #print sentences

  for index in range(len(sentences)):
    sentences[index] = ObjUnit.Sentence(sentences[index])

  return sentences
  #return ObjUnit.Sentence(text)

"""word = Word("montru")
print word.str_word, '\n'
print word.word_info, '\n'
print word.dict_word
"""
