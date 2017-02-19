# -*- coding: utf-8 -*-
import sys, os
from . import NLModules, relation, extractor, converter, BeautySafe

class LangClass():
  levels = ["graphmath", "morph", "postmorph", "synt", "extract", "convert"]
  def __init__(self, settings): # импорт модулей и выдача финуций.
    self.settings = settings
    self.language = settings['language']
    self.LangModule = NLModules.getLangModule(self.language)

  def NL2IL(self, sentences, levels="graphmath convert"):
    """ Второй аргумент - диапазон конвертирования от первого до последнего
        включительно через пробел. Если требуется сделать лишь один уровень,
        то можно указать только одно слово. Если указан только 'convert',
        то в качестве первого аргумента передаётся список извлечений."""
    BeautySafe.fwrite('\n\n'+'#'*100+'\n')
    BeautySafe.fwrite(levels+'\n')
    OR = relation.ObjRelation(self.language, self.settings['test'], self.settings['storage_version']) # не выносить в __init__! Объект работы с БД должен создаваться в том потоке, в котором и будет использован
    ErrorConvert = []

    # Парсим строку диапазона
    levels = levels.split()
    if len(levels)==1:
      level = levels.pop()
      if level[0] == ':': start_level, end_level = self.levels[0], level[1:]
      elif level[-1] == ':': start_level, end_level = level[:-1], self.levels[-1]
      else: start_level = end_level = level
    else: start_level, end_level = levels

    # Графематический анализ
    if start_level in self.levels[:1]:
      #print sentences
      BeautySafe.safe_NL(sentences)
      sentences = self.LangModule.getGraphmathA(sentences)
      BeautySafe.safe_sentences(sentences, 'GraphemathicAnalysis analysis')
      if end_level == self.levels[0]: return sentence

    # Морфологический анализ
    if start_level in self.levels[:2]:
      sentences = self.LangModule.getMorphA(sentences)
      with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
        flog.write('\n')
        for index, sentence in sentences: flog.write('sentence: %s\n' % sentence.getUnit('str')['fwords'])
        flog.write('\n')
      BeautySafe.safe_sentences(sentences, 'Morphological analysis')
      if end_level == self.levels[1]: return sentences

    # Постморфологичесий
    if start_level in self.levels[:3]: 
     sentences = self.LangModule.getPostMorphA(sentences)
     BeautySafe.safe_sentences(sentences, 'Postmorphological analysis')
     if end_level == self.levels[2]: return sentences

    # Синтаксический
    if start_level in self.levels[:4]:
      sentences = self.LangModule.getSyntA(sentences)
      BeautySafe.safe_sentences(sentences, 'Syntactic analysis')
      if end_level == self.levels[3]: return sentences

    # извлекаем прямое доп, подл, сказуемое, косв. доп
    if start_level in self.levels[:5]:
      #if not isinstance(sentences, ObjUnit.Text): sentences = ObjUnit.Text([sentences])
      for index, sentence in sentences:
        OR.addWordsToDBFromDictSentence(sentence.getUnit('dict'))
        Extract = extractor.Extract(self.settings['assoc_version'])
        sentences.subunit_info[index] = Extract(sentence) # заменяем объекты предложения на словари извлечений
      if end_level == self.levels[4]: return sentences

    # конвертируем анализы во внутренний язык
    if start_level in self.levels[:6]:
      _ILs = {}
      _ErrorConvert = {}
      for index, sentence in sentences:
        _ILs[index] = []
        Extraction2IL = converter.Extraction2IL(self.settings['assoc_version'])
        ILs, ErrorConvert = Extraction2IL(OR, self.settings, *sentence)
        for IL in ILs: BeautySafe.safe_IL(IL)
        _ILs[index].extend(ILs)
        for key in ErrorConvert:
          if not key in _ErrorConvert: _ErrorConvert[key] = []
          _ErrorConvert[key].extend(ErrorConvert[key])
      if end_level == self.levels[5]: return _ILs, _ErrorConvert

  def IL2NL(self, IL):
    #IL = Synthesizer.IL2resultA(IL)
    #result = LangModule.ResultA2NL(IL)
    #return NL
    return IL
