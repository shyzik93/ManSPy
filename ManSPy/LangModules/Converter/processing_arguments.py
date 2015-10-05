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
  print len(prevchildl), prevchildl
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
##########################################

def matchDefinitonsAndCircumstances(AM, data, OR, true_bases):
  for feature in AM['feature']:
    if feature['POSpeech'] != data['POSpeech']: continue # так как могут быть и прилагательные, и притяж. местоимения.
    for descr_base in data['base']:
      if OR.isWordInAbstractGroup(feature['base'], descr_base):
        true_bases.append(feature['base'])
        break

def matchSupplements(AM, data, Supplement, true_bases):
  for link in AM['link']:
    supplement = Supplement[link]
    #ATTENTION Необходимо проверить выполнение условия!
    if 'case' in data and 'case' not in supplement:
      return None
    true_bases.append(supplement['base'])

def matchArgument(OR, AnotherMembers, Supplement, data):
  """ Сверяет найденный аргумент с его описанием.
      Возвращает корень слова-аргумента """
  #print '     ----------------\nAnotheMembers:', AnotherMembers, '\n        ---------------'
  true_bases = []
  for AM in AnotherMembers.values():
    #print 'matching:', type(data['parentBase']),  type(AM['base'])
    if data['parentBase'] != AM['base']: continue
    # Если аргумент - это обстоятельство или определение
    if data['MOSentence'] in ['circumstance', 'definition']:
      matchDefinitonsAndCircumstances(AM, data, OR, true_bases)
    # Если аргумент - это косвенное дополнение. Здесь нужно сделать проверку на синонимы
    elif data['MOSentence'] == 'supplement':
      matchSupplements(AM, data, Supplement, true_bases)
  return true_bases

def findArguments(Subject, Predicate, DirectSupplement, Supplement, data, argdesc, rec=0):
  """ Ищет возможные аргументы.
      Точнее - вынимает начальные точки подчинительной связи членов. """
  if data['parentMOSentence'] == 'direct supplement':
    return DirectSupplement
  elif data['parentMOSentence'] == 'subject':
    return Predicate
  else:
    data = argdesc[data['parentLink']] # по индексу посредника в словаре аргументов
    AnotherMembers = findArguments(Subject, Predicate, DirectSupplement, Supplement, data, argdesc)
    for index, AM in AnotherMembers.items():
      links = AM['link']
      if len(links) != 0:
        link = links[0]
        return {link: Supplement[link]}
      else: return {}
    return {}

def getArguments(OR, Subject, Predicate, DirectSupplement, Supplement, argdesc):
  # Вынимаем аргументы
  #found_args = [{}]
  _found_args = {}
  
  for name, desc in argdesc.items():
    if 'int' in str(type(name)): continue # Слова-посредники - пропускаем.
    AM = findArguments(Subject, Predicate, DirectSupplement, Supplement, desc, argdesc)
    #if len(AM) == 0: if data['required']: ErrorConvert.append("Required argument \"%s\" is absent!" % name)
    true_bases = matchArgument(OR, AM, Supplement, desc)
    print '01. True bases:', true_bases
    #if not true_bases: ErrorConvert.append('Checking of argument \"%s\" isn\'t successful!' % name)#str(data['base']))
    if not true_bases: print 'Matching of argument \"%s\" isn\'t successful!' % name

    _found_args[name] = true_bases

    #index_arg = 0
    #for true_base in true_bases:
    #  if name in found_args[index_arg]:
    #    if index_arg == len(found_args)-1: found_args.append({})
    #    index_arg += 1
    #  found_args[index_arg][name] = true_base

  print '02. Found arguments: ', _found_args

  # умножение
  found_args = dmultiply(_found_args)
  # соответствие, если в предложении указано наречие "соответственно"
  # здесь должен быть этот код
  
  print '02.1. Found arguments: ', found_args

  return found_args

def checkArguments(found_args, argdesc, index_IL, ErrorConvert):
  # Дополняем словари аргументов
  '''index = index2 = 0
  for found_arg in found_args:
    if len(found_arg) > len(found_args[index]): index = index2
    index2 += 1
  index2 = 0
  for found_arg in found_args:
    if len(found_arg) < len(found_args[index]):
      big = found_args[index].copy()
      big.update(found_args[index2])
      found_args[index2] = big
    index2 += 1'''

  # Проверяем аргументы на наличие в абстр. группе, заменяем по таблице и добавляем в ЯВ
  true_args = []
  for found_arg in found_args:
    true_args.append([])
    ErrorConvert.append([])
    for name, desc in argdesc.items():
      if 'int' in str(type(name)): continue
      if name not in found_arg:
        if desc['required']: ErrorConvert[index_IL].append("Required argument \"%s\" is absent!" % name)
        continue
      if desc['argtable']:
        if found_arg[name] in desc['argtable']: found_arg[name] = desc['argtable'][found_arg[name]]
        else: ErrorConvert.append("Argument \"%s\" (found value \"%s\") is absent in argtable!" % (name, found_arg[name]))
    true_args[index_IL] = found_arg
    index_IL += 1
  print '03. True args:', true_args, '\n'
  return true_args

if __name__ == '__main__':
  #resl = copy([[10], [20], [30], [40]], [1,2,3,4])

  parentl = [[1, 2, 3, 4],
       [10, 20, 30, 40],
       [100, 200, 300, 400]]
  #multiply(parentl)

  #dparentl = {'a': [1, 2, 3, 4],
  #     'b': [10, 20, 30, 40],
  #     'c': [100, 200, 300, 400]}
  dparentl = {'a': [1, 2, 3, 4],
       'b': [10, 20, 30, 40],
       'c': [100, 200, 300, 400]}
  dmultiply(dparentl)
