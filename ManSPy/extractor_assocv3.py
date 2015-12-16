# -*- coding: utf-8 -*-

def Extract(sentence):
  ''' Разбивает предложение на предикат и его актанты.
      Именга переменных здесь и далее в программе:
        argument - это актант, перевод на английский
        arg - это аргумент функции, имеет такойже первод на английский, как и актант'''
  predicate = {} # сказуемые
  arguments = []  # ловосочетания
  print sentence.getUnit('str')['fwords']

  #for name, str_s in sentence.getUnit('str').items():
  #  print name, ':', str_s

  # Поиск сказуемого
  predicates = sentence.getByCharacteristic('MOSentence', 'predicate')
  sentence.delByIndexWithoutSync(*predicates.keys())

  # прямое дополнение может быть не только в винительном падеже - зависит от глагола
  for index, word in sentence.itemsUnit():
    if word['MOSentence'] != 'supplement':
      arguments.append({})
    arguments[-1][index] = word

  for argument in arguments:
    sentence.delByIndexWithoutSync(*argument.keys())

  if sentence.getUnit("dict"):
    print u"       Необработанные остатки 3 ФАСИФ \n", sentence.getUnit("dict")
    print "-"*10

  return predicates, arguments
