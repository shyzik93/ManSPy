# -*- coding: utf-8 -*-
""" Модуль разбивает ЯЕ-предложенпие на группы из членов предложений.
"""

def Extract(sentence):#, Recursion=0):
  """ Выделяем основные члены предложения """
  #TASK после каждого программного блока необходимо удалить неиспользуемые более переменные
  ErrorConvert = []

  # Всё, что не подчиненно прямому дополнению - обстоятельсттва!

  Predicate = {}
  DirectSupplement = {}
  Subject = {}
  Supplement = {}

  # Поиск сказуемого
  Predicate = sentence.getByCharacteristic('MOSentence', 'predicate')
  sentence.delByIndexWithoutSync(*Predicate.keys())
  if len(Predicate) == 0:
    #TASK в дальнейшем написать код, запрашивающий сказуемое (Какое действие делает этот субъект)
    ErrorConvert.append([0, 'Prediate is absent'])
    return Subject, Predicate, DirectSupplement, Supplement, ErrorConvert

  # Поиск прямого дополнения
  """for link in Predicate['link']:
    if sentence.GetSet(link, 'MOSentence') == 'direct supplement':
      DirectSupplement = sentence.GetAndDel(index)
      break"""
  DirectSupplement = sentence.getByCharacteristic('MOSentence', 'direct supplement')
  sentence.delByIndexWithoutSync(*DirectSupplement.keys())
  if len(DirectSupplement) == 0: pass # отсутствует (бывает такое)
  elif len(DirectSupplement) == 1: pass # присуствует, всё нормально
  #else: pass # такое тоже бывает. Необходимо их проверить на однородность

  # Поиск подлежащего
  Subject = sentence.getByCharacteristic('MOSentence', 'subject')
  sentence.delByIndexWithoutSync(*Subject.keys())
  if len(Predicate) == 0: pass # спросить, кто выполняет действие
  elif len(Predicate) == 1: pass
  else: pass

  # Все оставшиеся слова - косвенные дополнения
  #Supplement = sentence.getSentence("dict")
  Supplement = sentence.getByCharacteristic('MOSentence', 'supplement')
  sentence.delByIndexWithoutSync(*Supplement.keys())

  print "-"*10, "\n            Необработанные остатки \n", sentence.getSentence("dict")
  print "-"*30

  return Subject, Predicate, DirectSupplement, Supplement, ErrorConvert
