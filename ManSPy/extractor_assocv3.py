# -*- coding: utf-8 -*-
import pprint

def Extract(sentence):
  ''' Разбивает предложение на предикат и его актанты.
      Именга переменных здесь и далее в программе:
        argument - это актант, перевод на английский
        arg - это аргумент функции, имеет такойже первод на английский, как и актант'''
  predicate = {} # сказуемые
  arguments = []  # словосочетания (актанты)
  print sentence.getUnit('str')['fwords']
  #pprint.pprint(sentence.getUnit("dict"))

  # Поиск сказуемого
  predicates = sentence.getByCharacteristic('MOSentence', 'predicate')
  sentence.delByIndex(*predicates.keys())

  # прямое дополнение может быть не только в винительном падеже - зависит от глагола
  for index, word in sentence.itemsUnit():
    if word['MOSentence'] != 'supplement':
      arguments.append({})
    if not arguments: arguments.append({}) # если в актанте остутсвуют прямые дополнения
    arguments[-1][index] = word

  for argument in arguments:
    sentence.delByIndex(*argument.keys())

  if sentence.getUnit("dict"):
    print u"       Необработанные остатки 3 ФАСИФ \n", sentence.getUnit("dict")
    print "-"*10

  return predicates, arguments
