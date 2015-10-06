# -*- coding: utf-8 -*-
"""
"""
import multiply_lists

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
  _found_args = {}

  # Вынимаем аргументы  
  for name, desc in argdesc.items():
    if 'int' in str(type(name)): continue # Слова-посредники - пропускаем.
    AM = findArguments(Subject, Predicate, DirectSupplement, Supplement, desc, argdesc)
    print '00. Candidates for true bases:', AM
    true_bases = matchArgument(OR, AM, Supplement, desc)
    print '01. True bases:', true_bases
    _found_args[name] = true_bases

  print '02. Found arguments: ', _found_args
  # умножение
  found_args = multiply_lists.dmultiply(_found_args)
  # соответствие, если в предложении указано наречие "соответственно"
  # здесь должен быть этот код  
  print '02.1. Found arguments: ', found_args
  return found_args

def checkArguments(found_args, argdesc, index_IL, ErrorConvert):
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
