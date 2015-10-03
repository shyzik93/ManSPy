# -*- coding: utf-8 -*-
'''
Этот модуль выполняет комплексный анализ тескта на ЯЕ Эсперанто.
'''

from PrepearingText import Prepearing # для langModules/__init__.py
from MorphologicalAnalysis import getMorphA
from PostMorphologicalAnalysis import getPostMorphA
from SyntacticAnalysis import getSyntA

# у следующих функций и переменных - одинаковые имена для всех ЯЕ!

def AnalyseNLSentence(obj_sentence, start_level, end_level, levels, log_func=None):
  ''' Принимает объект предложения и возвращает его, но уже с анализами '''
  GrammarNazi = {}

  # Морфологический анализ
  if start_level == levels[0]:
    obj_sentence, GrammarNazi['morph'] = getMorphA(obj_sentence)
    if log_func != None: log_func(obj_sentence, 'Morphological analysis')
    if end_level == levels[0]: return obj_sentence, GrammarNazi

  # Постморфологичесий
  if start_level in levels[0:2]: 
   obj_sentence, GrammarNazi['post_morph'] = getPostMorphA(obj_sentence)
   if log_func != None: log_func(obj_sentence, 'Postmorphological analysis')
   if end_level == levels[1]: return obj_sentence, GrammarNazi

  # Синтаксический
  if start_level in levels:
    obj_sentence, GrammarNazi['synt'] = getSyntA(obj_sentence)
    if log_func != None: log_func(obj_sentence, 'Syntactic analysis')
    return obj_sentence, GrammarNazi

# Синтез предложения:
# 1. Формируем анализы на основе ЯВ
# 2. Синтезируем предложение
