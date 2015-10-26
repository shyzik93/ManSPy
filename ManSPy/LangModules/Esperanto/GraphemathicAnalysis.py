# -*- coding: utf-8 -*-
""" Графематический анализ текста.
    Словарь символа: {'symbol': Символ, 'type': 'letter' OR 'punctuation_mark' OR 'other'}
    Словарь слова: {'word': СписокСимволов}
"""

LowLetters = u"ABCĈDEFGĜHĤIJĴKLMNOPRSŜTUŬVZ"
UpLetters =  u"abcĉdefgĝhĥijĵklmnoprsŝtuŭvz"
punctuation_marks = u".,;:!?-'\""

ReplacedLetters = {u'cx' :u'ĉ', u'gx': u'ĝ', u'hx': u'ĥ',
           u'jx': u'ĵ', u'sx': u'ŝ', u'ux': u'ŭ',
           u'\t': u'', u'\n': u''}

class Word(object):
  def __init__(self, str_word, description):
    self.str_word = str_word
    self.description = description
    self.dict_word = {'word': self.str_word}
  def __setitem__(self, key, value):
    if not isinstance(key, str) and not isinstance(key, unicode): 'abc'[1] = 'd' # возбуждаем исключение
    self.dict_word[key] = value
  def __getitem__(self, key):
    if isinstance(key, str) or isinstance(key, unicode): return self.dict_word[key]
    return self.str_word[key]
  def __getslice__(self, lower, upper):
    return self.str_word[lower:upper]

def getGraphmathA(sentence, Sentenceclass):
  # Заменяем символы
  for k, v in ReplacedLetters.items(): sentence = sentence.replace(k, v)

  sentence = sentence.split() # должен возвращать список предложений, но пока - список слов
  return Sentenceclass(sentence)
