# -*- coding: utf-8 -*-
''' Модуль выполняет синтаксический анализ предложения

  Определяются члены предложения и устанавливаются связи слов.

  Добавляются новые ключи:
    'link' - синтаксическая связь с другим словом. Значение:
    список порядковых номеров подчинённых (т. е. тех, кто к нему относится)
    #[{'index': INTEGER, 'type': 'parent/slave'}]
    'MOSentence' - член предложения
'''

def forPronounAndNoun(case):
  ''' Определяет член предложения для имени существительного
      и притяжательного местоимепния по падежу '''
  if case == 'accusative': return 'direct supplement'
  elif case == 'nominative': return 'subject'
  else: return 'supplement'

def setMOS_ToSign(features, GrammarNazi):
  """ Определение члена предложения у признаков:
      прилагательного, наречия, """
  for feature in features:
    if feature['POSpeech'] == 'adjective' or (feature['POSpeech'] == 'pronoun' and feature['category'] == 'possessive'):
      feature['MOSentence'] = 'definition'
      if len(feature['feature']) > 0:
        setMOS_ToSign(feature['feature'], GrammarNazi)

    elif feature['POSpeech'] == 'adverb':
      feature['MOSentence'] = 'circumstance'
      if len(feature['feature']) > 0:
        setMOS_ToSign(feature['feature'], GrammarNazi)

def setMOSentence(index, sentence, GrammarNazi):
  word = sentence(index)

  if word['POSpeech'] == 'verb':
    word['MOSentence'] = 'predicate'
    if len(word['feature']) > 0:
      setMOS_ToSign(word['feature'], GrammarNazi)

  #ATTENTION обстоятельства, выраженные существительным, определяются в модуле
  # промежуточного анализа как наречие.
  elif word['POSpeech'] == 'noun':
    word['MOSentence'] = forPronounAndNoun(word['case'])
    if len(word['feature']) > 0:
      setMOS_ToSign(word['feature'], GrammarNazi)

  elif word['POSpeech'] == 'pronoun':
    if word['category'] == 'possessive':
      word['MOSentence'] = 'definition'    # ? Появилось определение
    elif word['category'] == 'personal':
      word['MOSentence'] = forPronounAndNoun(word['case'])
    else: word['MOSentence'] = '' # не притяжательное и не личное местоимение

  # прилагательное без существительного
  elif word['POSpeech'] == 'adjective': word['MOSentence'] = 'definition'  
  else: word['MOSentence'] = ''
  return index

def setLinks(index, sentence, GrammarNazi):
  ''' Устанавливает связи членов предложения. Обстоятельства и определения
      спрятаны в тех, к кому они относятся. Работаем лишь со сказуемым,
      подлежащим и дополнением. '''
  word = sentence(index)

  if word['MOSentence'] == 'predicate':
    # линкуем сказуемое и прямое дополнение
    index2 = index+1
    while index2 < sentence.getLen():
      if sentence(index2, 'MOSentence') == 'direct supplement':
        sentence.addLink(index, index2)
      elif sentence(index2, 'MOSentence') == 'predicate': break
      index2 += 1

  #TASK если у прямого дополнения нескеолько дополнений, то они проигнорируются
  elif word['MOSentence'] in ['direct supplement', 'supplement', 'subject']:
    # линкуем прямое дополнение и следующее после него косвенное дополнение
    index2 = index+1
    case = None
    while index2 < sentence.getLen():
      word2 = sentence(index2)
      if word2['MOSentence'] == 'supplement' and word2['case'] != "":
        """# остальные падежи, вероятно, будут означать, что косв. дополнение -
        # это обстоятельство, то есть относится к сказуемому.
        #if sentence(index2, 'case') in ['genetive']: sentence.addLink(index, index2)#word['link'].append(index2)"""
        if not case:
          case = word['case']
          sentence.addLink(index, index2)
        elif case :
          sentence.addLink(index, index2)
      elif word2['MOSentence'] in ['direct supplement', 'subject']: return index # это другой актант уже пойдёт.
      index2 += 1

  return index

def getSyntA(sentences, GrammarNazi):
  for sentence in sentences:
    # определяет члены предложения
    sentence.forAllWords(0, setMOSentence, GrammarNazi)
    # устанавливает связи членов предложения
    sentence.forAllWords(0, setLinks, GrammarNazi)

  return sentences
