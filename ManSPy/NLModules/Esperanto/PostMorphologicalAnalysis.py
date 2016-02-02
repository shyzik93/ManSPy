# -*- coding: utf-8 -*-
''' Модуль выполняет расширенный морфологический разбор слова,
    то есть на основе связей в предложении.
    По завершению удаляются все служебные части речи.
    Можно приступать к синтаксичекому анализу предложения.
    '''
from pprint import pprint
import eonums

def processArticle(GrammarNazi, word, sentence):
  if word['POSpeech'] == 'article': sentence.delByStep() # пока только удаляем

def processPreposition(GrammarNazi, word, sentence):
  if word['POSpeech'] != 'preposition': return
  left, right = sentence.getNeighbours()
  if right == None: sentence.delByStep()
  elif right['POSpeech'] in ['noun', 'pronoun', 'numeral']:
    sentence.getByStep(1, 'case', word['give_case'])
    sentence.delByStep()
  else:
    GrammarNazi.append('After preposition "'+word['word']+'" must be a noun or a pronoun or a cardinal numeral! Found '+str(sentence.getByStep(1)))

def processConjunction(GrammarNazi, word, sentence):
  if word['POSpeech'] != 'conjunction' or word['value'] != 'coordinating': return
  left, right = sentence.getNeighbours()
  if left == None or right == None: # если союз первый или последний в предложении
    sentence.delByStep()
  # сочинительный союз
  #if word['word'] == 'kaj': # заменить логическими символами (kaj = &)
  #print word['base']
  if left['POSpeech'] == right['POSpeech'] or \
     (left['POSpeech'] == 'noun' and right['POSpeech'] == 'pronoun' and right['category'] != 'possessive') or (right['POSpeech'] == 'noun' and left['POSpeech'] == 'pronoun' and left['category'] != 'possessive') or \
     ((left['POSpeech'] == 'pronoun' and left['category'] == 'possessive') and right['POSpeech'] == 'adjective') or ((right['POSpeech'] == 'pronoun' and right['category'] == 'possessive') and left['POSpeech'] == 'adjective'):
     #((left['POSpeech'] in ['pronoun', 'adjective'] and ('category' in left and left['category'] == 'possessive')) and right['POSpeech'] in ['pronoun', 'adjective']):
  #if ('case' in left and 'case' in right) and left['case'] == right['case']:
    if ('case' in right and right['case'] == 'accusative') and ('case' in left and left['case'] != 'accusative'):
      sentence.delByStep(jump_step=0)
      return
    # устанавливаем однородность
    sentence.addHomogeneous(-1, 1) # для дополнений
    sentence.delByStep() # удаляем союз
  #elif left['POSpeech'] == 'noun' and right['POSpeech'] == 'preposition':
  # Однородности нужны лишь для дополнения связей. В коверторе должны фигурировать лишь связи, но не однородности!

def processDefinition(GrammarNazi, word, sentence, indexes=None):
  if indexes == None: indexes = []
  #print 'findDefinition:', word['word'], index, sentence.getLen()
  if word['POSpeech'] == 'adjective' or (word['POSpeech'] == 'pronoun' and word['category'] == 'possessive') or word['POSpeech']=='numeral':
    indexes.append(sentence.currentIndex())
    if sentence.isLast(): return # завершаем цикл, ибо прилагательные без существительного. Их мы не удаляем, так как они могут следовать после глагола esti
    sentence.jumpByStep()
    processDefinition(GrammarNazi, sentence.getByStep(), sentence, indexes)
  elif word['POSpeech'] in ['noun'] and len(indexes) > 0: # если перед существительным стояли прилагательные
    sentence.addFeature(sentence.currentIndex(), *indexes)
    sentence.jumpByStep(-len(indexes))

def checkAdverbBefore(sentence):
  if sentence.position+1 >= sentence.getLen(): return False# т. е. является последним
  #if adverb['base'] == u'ankaŭ': # стоит перед словом, к которому относится
  return sentence.getByStep(1, 'POSpeech') in ['verb', 'adjective', 'adverb']
def checkAdverbAfter(sentence):
  if sentence.isFirst(): return False
  return sentence.getByStep(-1, 'POSpeech') in ('verb', 'adjective', 'adverb')

def processAdverb(GrammarNazi, word, sentence):
  if sentence.getByStep()['POSpeech'] != 'adverb': return
  index = sentence.currentIndex()
  if checkAdverbBefore(sentence): # порядок менять не рекомендуется: покажи ОЧЕНЬ СИНИЙ цвет.
    # ПОКАЖИ БЫСТРО синий цвет - а вот здесь необходимо расставлять приоритеты для прилагательных и глаголов.
    # БЫСТРО - относится только к глаголам,
    # ПОКАЖИ ОЧЕНЬ синий цвет - стоит перед словом, к которому относится (глагол, наречие, прил)
    # ХОЧУ ОЧЕНЬ СИЛЬНО ; ХОЧУ ОЧЕНЬ - одно и тоже, но в первом случае
    # ОЧЕНЬ относится к СИЛЬНО, а СИЛЬНО - к глаголу. В овтором случае - ОЧЕНЬ относится к глаголу.
    # то есть, одни наречия для прилагательных, другие - для глаголов.
    sentence.addFeature(index+1, index)
  elif checkAdverbAfter(sentence):
    sentence.addFeature(index-1, index)
    sentence.jumpByStep(-1)
  else:
    old_position = sentence.position
    for index2, word in sentence: # "свободноплавающее" нарчие. Добавим его к глаголу.
      if word['POSpeech'] == 'verb':
        sentence.addFeature(index2, index) #EX_ERROR если последний  index2, то возникает интересная рекурсивная ошибка.
        break
    sentence.position = old_position
    #Error print index бесконечный цикл, если в предложении одни только наречия. Решение - сделать добавление мнимых слов.

def exchangeDataBetweenHomo(sentence):
  done_indexes = []
  for index, word in sentence:
    if index in done_indexes: continue
    index_homos = word['homogeneous_link']
    for index_homo in index_homos:
      if 'case' in word: sentence(index_homo, 'case', word['case'])
      done_indexes.append(index_homo)

def processNumeral(GrammarNazi, word, sentence, indexes=None):
  if indexes == None: indexes = []
  if word['POSpeech'] == 'numeral':
    indexes.append(sentence.currentIndex())
    if not sentence.isLast():
      sentence.jumpByStep()
      processNumeral(GrammarNazi, sentence.getByStep(), sentence, indexes)
      return
  if len(indexes) <= 1: return

  # "Склейка" числительных
  print indexes
  glued_numeral = ' '.join([sentence(index, 'word') for index in indexes])
  print glued_numeral
  sentence(indexes[-1], 'word', glued_numeral)
  sentence(indexes[-1], 'number_value', eonums.eo2int(glued_numeral))
  sentence(indexes[-1], 'base', '')
  sentence.delByIndex(*indexes[:-1])
  sentence.jumpByStep(-len(indexes))

def runScript(GrammarNazi, sentence, names):
  names = names.split()
  for name in names:
    func = globals()['process'+name]
    for index, word in sentence: func(GrammarNazi, word, sentence)

def getPostMorphA(sentences, GrammarNazi):
  ''' Обёртка '''
  for index, sentence in sentences:
    #TASK обстоятельства, выраженные существительным, обозначить как наречие
    runScript(GrammarNazi, sentence, 'Numeral Article Conjunction Adverb Conjunction Definition Conjunction Preposition Conjunction')
    exchangeDataBetweenHomo(sentence) # копируем характеристики с первого однородного ко последующим ему однородным.

    # здесь нужно найти однородные косвенные дополнения, чтобы им установить однородность.
    # При синтаксическом анализе на них будет ссылаться их родитель.

  return sentences
