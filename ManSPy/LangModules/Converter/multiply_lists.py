# -*- coding: utf-8 -*-
"""
"""

def copy(resl, addl):
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

def multiply(parentl):
  prevchildl = [[]]
  for childl in parentl:
    prevchildl = copy(prevchildl, childl)
  #print len(prevchildl), prevchildl
  return prevchildl

def dcopy(resl, addl, name):
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

def dmultiply(dparentl):
  prevchildl = [{}]
  for name, childl in dparentl.items():
    prevchildl = dcopy(prevchildl, childl, name)
  #print len(prevchildl), prevchildl
  return prevchildl

if __name__ == '__main__':
  #resl = copy([[10], [20], [30], [40]], [1,2,3,4])

  parentl = [[1, 2, 3, 4],
       [10, 20, 30, 40],
       [100, 200, 300, 400]]
  resl = multiply(parentl)
  print len(resl), resl

  dparentl = {'a': [1, 2, 3, 4],
       'b': [10, 20, 30, 40],
       'c': [100, 200, 300, 400]}
  resl = dmultiply(dparentl)
  print len(resl), resl

  parentl = ['a', 'b', 'c']
  parentl = [parentl] * len(parentl)
  resl = multiply(parentl)
  print len(resl), [''.join(r) for r in resl]
