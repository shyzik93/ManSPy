# -*- coding: utf-8 -*-
import sys, os

_path = os.path.dirname(__file__)
sys.path.append(_path)

import extractor, converter, ObjUnit, relation
import BeautySafe

class LangClass():
  levels = ["graphmath", "morph", "postmorph", "synt", "extract", "convert"]
  def __init__(self, settings, Action): # импорт модулей и выдача финуций.
    self.settings = settings
    self.language = settings['language']
    self.LangModule = __import__(self.language)
    self.Action = Action

  def NL2IL(self, sentences, levels="graphmath convert"):
    """ Второй аргумент - диапазон конвертирования от первого до последнего
        включительно через пробел. Если требуется сделать лишь один уровень,
        то можно указать только одно слово. Если указан только 'convert',
        то в качестве первого аргумента передаётся список извлечений."""
    BeautySafe.fwrite('\n\n'+'#'*100+'\n')
    BeautySafe.fwrite(levels+'\n')
    OR = relation.ObjRelation(self.language, self.settings['test'], self.settings['storage_version']) # не выносить в __init__! Объект работы с БД должен создаваться в том потоке, в котором и будет использован
    GrammarNazi = {'morph': [], 'postmorph': [], 'synt': []}
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
      BeautySafe.safe_NL(sentences)
      sentences = self.LangModule.getGraphmathA(sentences, ObjUnit)
      BeautySafe.safe_sentences(sentences, 'GraphemathicAnalysis analysis')
      if end_level == self.levels[0]: return sentence, GrammarNazi

    # Морфологический анализ
    if start_level in self.levels[:2]:
      sentences = self.LangModule.getMorphA(sentences, GrammarNazi['morph'])
      BeautySafe.safe_sentences(sentences, 'Morphological analysis')
      if end_level == self.levels[1]: return sentences, GrammarNazi

    # Постморфологичесий
    if start_level in self.levels[:3]: 
     sentences = self.LangModule.getPostMorphA(sentences, GrammarNazi['postmorph'])
     BeautySafe.safe_sentences(sentences, 'Postmorphological analysis')
     if end_level == self.levels[2]: return sentences, GrammarNazi

    # Синтаксический
    if start_level in self.levels[:4]:
      sentences = self.LangModule.getSyntA(sentences, GrammarNazi['synt'])
      BeautySafe.safe_sentences(sentences, 'Syntactic analysis')
      if end_level == self.levels[3]: return sentences, GrammarNazi

    # извлекаем прямое доп, подл, сказуемое, косв. доп
    if start_level in self.levels[:5]:
      if not isinstance(sentences, list): sentences = [sentences]
      for index in range(len(sentences)):
        sentence = sentences[index]
        OR.addWordsToDBFromDictSentence(sentence.getUnit('dict'))
        #Subject, Predicate, DirectSupplement, Supplement, ErrorConvert = Extractor.Extract(sentence)
        Extract = extractor.Extract(self.settings['assoc_version'])
        sentences[index] = Extract(sentence)
      if end_level == self.levels[4]: return sentences#return Subject, Predicate, DirectSupplement, Supplement, GrammarNazi, ErrorConvert

    # конвертируем анализы во внутренний язык
    if start_level in self.levels:
      #if start_level == self.levels[:6]: Subject, Predicate, DirectSupplement, Supplement = sentence
      _ILs = []
      _ErrorConvert = {}
      for sentence in sentences:
        #ILs, ErrorConvert = Converter.Extraction2IL(OR, self.settings, self.Action, Subject, Predicate, DirectSupplement, Supplement)
        Extraction2IL = converter.Extraction2IL(self.settings['assoc_version'])
        ILs, ErrorConvert = Extraction2IL(OR, self.settings, self.Action, *sentence)
        for IL in ILs: BeautySafe.safe_IL(IL)
        _ILs.extend(ILs)
        for key in ErrorConvert:
          if not key in _ErrorConvert: _ErrorConvert[key] = []
          _ErrorConvert[key].extend(ErrorConvert[key])
      if end_level == self.levels[5]: return _ILs, GrammarNazi, _ErrorConvert

  def IL2NL(self, IL):
    #IL = Synthesizer.IL2resultA(IL)
    #result = LangModule.ResultA2NL(IL)
    #return NL
    return IL
