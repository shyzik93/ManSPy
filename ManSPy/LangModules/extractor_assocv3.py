# -*- coding: utf-8 -*-

def Extract(sentence):
  Subject = {}
  Predicate = {}
  Object = {}

  # Поиск сказуемого
  Predicate = sentence.getByCharacteristic('MOSentence', 'predicate')
  sentence.delByIndexWithoutSync(*Predicate.keys())
  if len(Predicate) == 0:
    ErrorConvert.append([0, 'Prediate is absent'])
    return Subject, Predicate, DirectSupplement, Supplement, ErrorConvert

  # Поиск прямого дополнения (только для первого сказуемого)
  for index_predic, predic in Predicate.items():
    for link in predic['link']:
      if sentence(link, 'MOSentence') == 'direct supplement':
        DirectSupplement[link] = sentence(link)
    break
  sentence.delByIndexWithoutSync(*DirectSupplement.keys())

  # Поиск подлежащего
  Subject = sentence.getByCharacteristic('MOSentence', 'subject')
  sentence.delByIndexWithoutSync(*Subject.keys())

  # Все оставшиеся слова - косвенные дополнения
  #Supplement = sentence.getSentence("dict")
  Supplement = sentence.getByCharacteristic('MOSentence', 'supplement')
  sentence.delByIndexWithoutSync(*Supplement.keys())

  if sentence.getUnit("dict"):
    print u"       Необработанные остатки \n", sentence.getUnit("dict")
    print "-"*10

  return Subject, Predicate, Object
