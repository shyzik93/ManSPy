# -*- coding: utf-8 -*-
''' Модуль выполняет расширенный морфологический разбор слова,
    то есть на основе связей в предложении.
    По завершению удаляются все служебные части речи.
    Можно приступать к синтаксичекому анализу предложения.
    '''

def processingPreposition(GrammarNazi, index, sentence):
  preposition = sentence(index)
  if preposition['POSpeech'] != 'preposition': return
  left, right = sentence.getSurroundingNeighbours(index)
  if right == None: sentence.delByIndex(index)
  elif right['POSpeech'] in ['noun', 'pronoun']:
    sentence(index+1, 'case', preposition['give_case'])
  else:
    GrammarNazi.append('After preposition "'+preposition['word']+'" must be a noun or a pronoun!')

def processingConjunction(GrammarNazi, index, sentence):
  conjunction = sentence(index)
  if conjunction['POSpeech'] != 'conjunction' or conjunction['value'] != 'coordinating':
    return index + 1
  left, right = sentence.getSurroundingNeighbours(index)
  if left == None or right == None: # если союз первый или последний в предложении
    sentence.delByIndex(index)
    return index
  # сочинительный союз
  #if conjunction['word'] == 'kaj': # заменить логическими символами (kaj = &)
  #print conjunction['base']
  if left['POSpeech'] == right['POSpeech'] or \
     (left['POSpeech'] == 'noun' and right['POSpeech'] == 'pronoun' and right['category'] != 'possessive') or (right['POSpeech'] == 'noun' and left['POSpeech'] == 'pronoun' and left['category'] != 'possessive') or \
     ((left['POSpeech'] == 'pronoun' and left['category'] == 'possessive') and right['POSpeech'] == 'adjective') or ((right['POSpeech'] == 'pronoun' and right['category'] == 'possessive') and left['POSpeech'] == 'adjective'):
     #((left['POSpeech'] in ['pronoun', 'adjective'] and ('category' in left and left['category'] == 'possessive')) and right['POSpeech'] in ['pronoun', 'adjective']):
  #if ('case' in left and 'case' in right) and left['case'] == right['case']:
    if ('case' in right and right['case'] == 'accusative') and ('case' in left and left['case'] != 'accusative'):
      sentence.delByIndex(index)
      return index+1
    # устанавливаем однородность
    sentence.addHomogeneous(index-1, index+1) # для дополнений
    #if 'case' in left: sentence(index-1, 'case', sentence(index+1, 'case')) # копируем характеристики с первого однородного на второе
    sentence.delByIndex(index) # удаляем союз
    return index # the same right-1
  return index + 1
  #elif left['POSpeech'] == 'noun' and right['POSpeech'] == 'preposition':
  # Однородности нужны лишь для дополнения связей. В коверторе должны фигурировать лишь связи, но не однородности!

def findDefinitions(GrammarNazi, index, sentence, indexes=[]):
  """ Поиск определений. Аргумент index - это индекс первого определения """
  word = sentence(index)
  #print 'findDefinition:', word['word'], index, sentence.getLen()
  if word['POSpeech'] == 'adjective' or (word['POSpeech'] == 'pronoun' and word['category'] == 'possessive'):
    indexes.append(index)
    if index == sentence.getLen()-1: return index + 1 # завершаем цикл, ибо прилагательные без существительного. Их мы не удаляем, так как они могут следовать после глагола esti
    return findDefinitions(GrammarNazi, index+1, sentence, indexes) + 1
  elif word['POSpeech'] in ['noun'] and len(indexes) > 0: # если перед существительным стояли прилагательные
    return sentence.addFeature(index, *indexes)
  else: return index + 1

def procPrep(GrammarNazi, sentence):
  index = 0
  while index < sentence.getLen():
    processingPreposition(GrammarNazi, index, sentence)
    index += 1

def procConj(GrammarNazi, sentence):
  index = 0
  #print 'CONJUCTION'
  while index < sentence.getLen():
    index = processingConjunction(GrammarNazi, index, sentence)

def findDef(GrammarNazi, sentence):
  index = 0
  while index < sentence.getLen():
    index = findDefinitions(GrammarNazi, index, sentence, [])

def checkAdverbBefore(index, sentence):
  if index+1 >= sentence.getLen(): return False# т. е. является последним
  #if adverb['base'] == u'ankaŭ': # стоит перед словом, к которому относится
  return sentence(index+1, 'POSpeech') in ['verb', 'adjective', 'adverb']
def checkAdverbAfter(index, sentence):
  if index == 0: return False
  return sentence(index-1, 'POSpeech') in ['verb', 'adjective', 'adverb']
def checkAdverb(index, sentence):
  if checkAdverbBefore(index, sentence): # порядок менять не рекомендуется: покажи ОЧЕНЬ СИНИЙ цвет.
    # ПОКАЖИ БЫСТРО синий цвет - а вот здесь необходимо расставлять приоритеты для прилагательных и глаголов.
    # БЫСТРО - относится только к глаголам,
    # ПОКАЖИ ОЧЕНЬ синий цвет - стоит перед словом, к которому относится (глагол, наречие, прил)
    # ХОЧУ ОЧЕНЬ СИЛЬНО ; ХОЧУ ОЧЕНЬ - одно и тоже, но в первом случае
    # ОЧЕНЬ относится к СИЛЬНО, а СИЛЬНО - к глаголу. В овтором случае - ОЧЕНЬ относится к глаголу.
    # то есть, одни наречия для прилагательных, другие - для глаголов.
    sentence.addFeature(index+1, index)
    index += 1
  elif checkAdverbAfter(index, sentence):
    sentence.addFeature(index-1, index)
    index -= 1
  else:
    index2 = 0 # "свободноплавающее" нарчие. Добавим его к глаголу.
    while index2 < sentence.getLen():
      if sentence(index2, 'POSpeech') == 'verb':
        sentence.addFeature(index2, index) #EX_ERROR если последний  index2, то возникает интересная рекурсивная ошибка.
        break
      index2 += 1
    index += 1
  return index
def checkAd(sentence):
  index = 0
  while index < sentence.getLen():
    if sentence(index, 'POSpeech') == 'adverb':
      index = checkAdverb(index, sentence)
      #Error print index бесконечный цикл, если в предложении одни только наречия. Решение - сделать добавление мнимых слов.
    else: index += 1

def exchangeDataBetweenHomo(sentence):
  index = -1
  done_indexes = []
  while index < sentence.getLen()-1:
    index += 1
    if index in done_indexes: continue
    word = sentence(index)
    index_homos = word['homogeneous_link']
    for index_homo in index_homos:
      if 'case' in word: sentence(index_homo, 'case', word['case'])
      done_indexes.append(index_homo)

def getPostMorphA(sentences, GrammarNazi):
  ''' Обёртка '''
  for sentence in sentences:
    #TASK обстоятельства, выраженные существительным, обозначить как наречие

    procConj(GrammarNazi, sentence) # rapido kaj ankaux, dolaran kaj euxran, lampo kaj fortreno

    # сворачиваем все наречия, даже многократно вложенные.
    while sentence.getByCharacteristic('POSpeech', 'adverb') != {}: checkAd(sentence)

    procConj(GrammarNazi, sentence) # montru [rapido] kaj inkludu

    # "Сворачиваем" признак предмета: прилагательные и притяжательные местоимения -
    findDef(GrammarNazi, sentence)

    # вот здесь нужно свернуть найденные однородные существительные
    procConj(GrammarNazi, sentence) # cxambro kaj [mia] domo

    procPrep(GrammarNazi, sentence) # Корректируем падежи
    sentence.delByCharacteristic('POSpeech', 'preposition') # удаляем предлоги

    procConj(GrammarNazi, sentence) # cxambro [en] domo
    exchangeDataBetweenHomo(sentence) # копируем характеристики с первого однородного ко последующим ему однородным.

    # здесь нужно найти однородные косвенные дополнения, чтобы им установить однородность.
    # При синтаксическом анализе на них будет ссылаться их родитель.

  return sentences
