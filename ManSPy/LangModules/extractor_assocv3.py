# -*- coding: utf-8 -*-

def Extract(sentence):
  predicate = {} # сказуемые
  w_combins = []  # ловосочетания

  for name, str_s in sentence.getUnit('str').items():
    print name, ':', str_s

  # Поиск сказуемого
  predicates = sentence.getByCharacteristic('MOSentence', 'predicate')
  sentence.delByIndexWithoutSync(*predicates.keys())

  # прямое дополнение может быть не только в винительном падеже - зависит от глагола
  for index, word in sentence.itemsUnit():
    if word['MOSentence'] != 'supplement':
      w_combins.append({})
    w_combins[-1][index] = word

  for w_combin in w_combins:
    sentence.delByIndexWithoutSync(*w_combin.keys())

  print w_combins

  if sentence.getUnit("dict"):
    print u"       Необработанные остатки \n", sentence.getUnit("dict")
    print "-"*10

  return predicates, w_combins
