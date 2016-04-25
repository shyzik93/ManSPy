# -*- coding: utf-8 -*-
''' Модуль математической лингвистии '''

def _product(resl, addl):
  n = len(addl)
  #_resl = list(resl)
  _resl = []
  for i, el in enumerate(resl, 0):
    _resl.insert(0, list(el))
    for j in range(n-1): _resl.insert(0, list(el))
    #print _resl
    for j in range(n): _resl[j].append(addl[j])
    #print _resl
  #print len(_resl), _resl, '\n'
  return _resl

def product(parentl):
  ''' Выполняет декартово (прямое) произведение над списками в списке parent1
      В стандартной библиотеке Python есть модуль, в котором уже есть реализация данного алгоритма. '''
  prevchildl = [[]]
  for childl in parentl:
    prevchildl = _product(prevchildl, childl)
  #print len(prevchildl), prevchildl
  return prevchildl

def _dproduct(resl, addl, name):
  n = len(addl)
  _resl = list(resl)
  for i, el in enumerate(resl, 0):
    #_resl.insert(0, [])
    for j in range(n-1): _resl.insert(i*n, dict(el))
    #print _resl
    for j in range(n): _resl[j+n*i][name] = addl[j]#.append(addl[j])
    #print _resl
  #print len(_resl), _resl, '\n'
  return _resl

def dproduct(dparentl):
  ''' Выполняет декартово (прямое) произведение над словарями в списке dparent1
      {'a': [1,2], 'b': [5,6]} -> [{'a': 1, 'b':5}, {'a': 1, 'b':6}, {'a': 2, 'b':5}, {'a': 2, 'b':6}]
      В стандартной библиотеке Python я этой функции не нашёл.
      Функция необходима для аргументных слов.
  '''
  prevchildl = [{}]
  for name, childl in dparentl.items():
    prevchildl =_dproduct(prevchildl, childl, name)
  #print len(prevchildl), prevchildl
  return prevchildl

#def is_antonym(is_antonym, has_antonym_prefix):
#  return is_antonym != has_antonym_prefix

if __name__ == '__main__':
  #resl = copy([[10], [20], [30], [40]], [1,2,3,4])

  parentl = [[1, 2, 3, 4],
       [10, 20, 30, 40],
       [100, 200, 300, 400]]
  resl = product(parentl)
  print(len(resl), resl)

  dparentl = {'a': [1, 2, 3, 4],
       'b': [10, 20, 30, 40],
       'c': [100, 200, 300, 400]}
  resl = dproduct(dparentl)
  print(len(resl), resl)

  parentl = ['a', 'b', 'c']
  parentl = [parentl] * len(parentl)
  resl = product(parentl)
  print(len(resl), [''.join(r) for r in resl])
