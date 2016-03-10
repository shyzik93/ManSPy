# -*- coding: utf-8 -*-
""" Модуль разбивает ЯЕ-предложенпие на группы из членов предложений.
"""

def Extract(sentence):#, Recursion=0):
  """ Выделяем основные члены предложения """
  #TASK после каждого программного блока необходимо удалить неиспользуемые более переменные

  # Всё, что не подчиненно прямому дополнению - обстоятельсттва!

  Predicate = {}
  DirectSupplement = {}
  Subject = {}
  Supplement = {}

  # Поиск сказуемого
  Predicate = sentence.getByCharacteristic('MOSentence', 'predicate')
  sentence.delByIndex(*Predicate.keys())
  if len(Predicate) == 0:
    #TASK в дальнейшем написать код, запрашивающий сказуемое (Какое действие делает этот субъект)
    #ErrorConvert.append([0, 'Prediate is absent'])
    return Subject, Predicate, DirectSupplement, Supplement, ErrorConvert

  # Поиск прямого дополнения (только для первого сказуемого)
  for index_predic, predic in Predicate.items():
    for link in predic['link']:
      if sentence(link, 'MOSentence') == 'direct supplement':
        #DirectSupplement = sentence.GetAndDel(link)
        DirectSupplement[link] = sentence(link)
    break
  #DirectSupplement = sentence.getByCharacteristic('MOSentence', 'direct supplement') # не удалять пока!
  sentence.delByIndex(*DirectSupplement.keys())
  #if len(DirectSupplement) == 0: pass # отсутствует (бывает такое)
  #elif len(DirectSupplement) == 1: pass # присуствует, всё нормально
  #else: pass # такое тоже бывает. Необходимо их проверить на однородность

  # Поиск подлежащего
  Subject = sentence.getByCharacteristic('MOSentence', 'subject')
  sentence.delByIndex(*Subject.keys())

  # Все оставшиеся слова - косвенные дополнения
  #Supplement = sentence.getSentence("dict")
  Supplement = sentence.getByCharacteristic('MOSentence', 'supplement')
  sentence.delByIndex(*Supplement.keys())

  if sentence.getUnit("dict"):
    print u"       Необработанные остатки 2 ФАСИФ\n", sentence.getUnit("dict")
    print "-"*10

  return Subject, Predicate, DirectSupplement, Supplement
