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

def setMOSentence(word, sentence, GrammarNazi):
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

def setLinks(index, sentence, GrammarNazi):
  ''' Устанавливает связи членов предложения. Обстоятельства и определения
      спрятаны в тех, к кому они относятся. Работаем лишь со сказуемым,
      подлежащим и дополнением. '''
  word = sentence(index)

  if word['MOSentence'] == 'predicate':
    # линкуем сказуемое и прямое дополнение
    old_position = sentence.position
    for index2, word2 in sentence.iterFrom(1):
      if sentence(index2, 'MOSentence') == 'direct supplement':
        sentence.addLink(index, index2)
      elif sentence(index2, 'MOSentence') == 'predicate': break
    sentence.position = old_position

  #TASK если у прямого дополнения нескеолько дополнений, то они проигнорируются
  elif word['MOSentence'] in ['direct supplement', 'supplement', 'subject']:
    # линкуем прямое дополнение и следующее после него косвенное дополнение
    old_position = sentence.position
    case = None
    for index2, word2 in sentence.iterFrom(1):
      if word2['MOSentence'] == 'supplement' and word2['case'] != "":
        """# остальные падежи, вероятно, будут означать, что косв. дополнение -
        # это обстоятельство, то есть относится к сказуемому.
        #if sentence(index2, 'case') in ['genetive']: sentence.addLink(index, index2)#word['link'].append(index2)"""
        if not case:
          case = word['case']
          sentence.addLink(index, index2)
        elif case :
          sentence.addLink(index, index2)
      elif word2['MOSentence'] in ['direct supplement', 'subject']:
        break # это другой актант уже пойдёт.
    sentence.position = old_position

def getSyntA(sentences, GrammarNazi):
  for index, sentence in sentences:
    # определяет члены предложения
    for index, word in sentence: setMOSentence(word, sentence, GrammarNazi)
    # устанавливает связи членов предложения
    for index, word in sentence: setLinks(index, sentence, GrammarNazi)

  return sentences
