# -*- coding: utf-8 -*-
""" 
"""
import sys, os

_path = os.path.dirname(__file__)
sys.path.append(_path)

import Extractor, Converter, ObjUnit, ObjRelation
import BeautySafe

class LangClass():
  levels = ["graphmath", "morph", "postmorph", "synt", "extract", "convert"]
  def __init__(self, settings, Action): # импорт модулей и выдача финуций.
    self.settings = settings
    self.language = settings['language']
    self.LangModule = __import__(self.language)
    self.Action = Action

  def NL2IL(self, sentence, levels="graphmath convert"):
    """ Второй аргумент - диапазон конвертирования от первого до последнего
        включительно через пробел. Если требуется сделать лишь один уровень,
        то можно указать только одно слово. Если указан только 'convert',
        то в качестве первого аргумента передаётся список извлечений."""
    BeautySafe.fwrite('\n\n'+'#'*100+'\n')
    BeautySafe.fwrite(levels+'\n')
    OR = ObjRelation.ObjRelation(self.language, self.settings['test'], self.settings['storage_version']) # не выносить в __init__! Объект работы с БД должен создаваться в том потоке, в котором и будет использован

    levels = levels.split()
    if len(levels)==1:
      level = levels.pop()
      if level[0] == ':': start_level, end_level = self.levels[0], level[1:]
      elif level[-1] == ':': start_level, end_level = level[:-1], self.levels[-1]
      else: start_level = end_level = level
    else: start_level, end_level = levels

    GrammarNazi = ErrorConvert = []

    #if start_level == self.levels[0]:
      # подгатавливаем текст
      #BeautySafe.safe_NL(sentence)
      #sentence = self.LangModule.Prepearing(sentence, ObjUnit.Sentence)
      # возвращаем предложения в виде объекта
      #sentence = ObjUnit.Sentence(list_sentence)

    # делаем полный морфологический и синтаксический анализы
    if start_level in self.levels[0:4]:
      BeautySafe.safe_NL(sentence)
      sentence, GrammarNazi = self.LangModule.AnalyseNLSentence(sentence, start_level, end_level, self.levels, ObjUnit.Sentence, BeautySafe.safe_sentence)
      if end_level in self.levels[0:4]: return sentence, GrammarNazi

    # извлекаем прямое доп, подл, сказуемое, косв. доп
    if start_level in self.levels[0:5]:
      OR.addWordsToDBFromDictSentence(sentence.getSentence('dict'))
      Subject, Predicate, DirectSupplement, Supplement, ErrorConvert = Extractor.Extract(sentence)
      if end_level == self.levels[4]: return Subject, Predicate, DirectSupplement, Supplement, GrammarNazi, ErrorConvert

    if start_level in self.levels:
      # конвертируем анализы во внутренний язык
      if start_level == self.levels[5]: Subject, Predicate, DirectSupplement, Supplement = sentence
      ILs, ErrorConvert = Converter.Extraction2IL(OR, self.settings, self.Action, Subject, Predicate, DirectSupplement, Supplement)
      for IL in ILs: BeautySafe.safe_IL(IL)
      if end_level == self.levels[5]: return ILs, GrammarNazi, ErrorConvert

  def IL2NL(self, IL):
    #IL = Synthesizer.IL2resultA(IL)
    #result = LangModule.ResultA2NL(IL)
    #return NL
    return IL
