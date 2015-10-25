# -*- coding: utf-8 -*-
""" Модуль подготовительной обработки текста. Задача:разбить текст на предложения;
    выделить данные в кавычках;
    разбить сложные предложения на простые, ориентируясь по союзам.
"""

def getGraphmathA(sentence, Sentenceclass):
  # Заменяем символы
  letters = {u'cx' :u'ĉ', u'gx': u'ĝ', u'hx': u'ĥ',
             u'jx': u'ĵ', u'sx': u'ŝ', u'ux': u'ŭ',
             u'\t': u'', u'\n': u''}
  for k, v in letters.items(): sentence = sentence.replace(k, v)

  sentence = sentence.split() # должен возвращать список предложений, но пока - список слов
  return Sentenceclass(sentence)
