# -*- coding: utf-8 -*-
'''
Этот модуль выполняет комплексный анализ тескта на ЯЕ Эсперанто.
'''

from GraphemathicAnalysis import getGraphmathA
from MorphologicalAnalysis import getMorphA
from PostMorphologicalAnalysis import getPostMorphA
from SyntacticAnalysis import getSyntA

# у следующих функций и переменных - одинаковые имена для всех ЯЕ!

def AnalyseNLSentence(sentence, start_level, end_level, levels, sentenceclass, log_func=None):
  ''' Принимает объект предложения и возвращает его, но уже с анализами '''
  GrammarNazi = {}

  # Графематический анализ
  if start_level == levels[0]:
    sentence = getGraphmathA(sentence, sentenceclass)
    if log_func != None: log_func(sentence, 'GraphemathicAnalysis analysis')
    if end_level == levels[0]: return sentence, GrammarNazi

  # Морфологический анализ
  if start_level in levels[:2]:
    sentence, GrammarNazi['morph'] = getMorphA(sentence)
    if log_func != None: log_func(sentence, 'Morphological analysis')
    if end_level == levels[1]: return sentence, GrammarNazi

  # Постморфологичесий
  if start_level in levels[:3]: 
   sentence, GrammarNazi['postmorph'] = getPostMorphA(sentence)
   if log_func != None: log_func(sentence, 'Postmorphological analysis')
   if end_level == levels[2]: return sentence, GrammarNazi

  # Синтаксический
  if start_level in levels:
    sentence, GrammarNazi['synt'] = getSyntA(sentence)
    if log_func != None: log_func(sentence, 'Syntactic analysis')
    return sentence, GrammarNazi

# Синтез предложения:
# 1. Формируем анализы на основе ЯВ
# 2. Синтезируем предложение
