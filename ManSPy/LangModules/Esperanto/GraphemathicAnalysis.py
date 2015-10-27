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

def getGraphmathA(sentence, ObjUnit):
  # Заменяем символы
  for k, v in ReplacedLetters.items(): sentence = sentence.replace(k, v)
  sentence = sentence.split() # должен возвращать список предложений, но пока - список слов
  sentence = [ObjUnit.Word(word) for word in sentence]

  return ObjUnit.Sentence(sentence)

"""word = Word("montru")
print word.str_word, '\n'
print word.word_info, '\n'
print word.dict_word
"""
