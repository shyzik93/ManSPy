# -*- coding: utf-8 -*-
"""
"""
import os, copy
from .. import common, lingvo_math

def walk(o, func, parent=None, key=None):
  if isinstance(o, dict): keys = o.keys()
  elif isinstance(o, list): keys = range(len(o))
  else:
    if parent != None: parent[key] = func(o)
    return

  for key in keys:
    walk(o[key], func, parent=o, key=key)

def func(o):
  #print type(o), o
  if hasattr(o, '__str__') and hasattr(o, 'items'): return str(o)
  return o

def write_log(*texts):
  path = os.path.join(common.RSettings('dir_db'), 'args.txt')#os.path.join(os.path.abspath(''), 'args.txt')
  if not os.path.exists(path):
    with open(path, 'w'): pass
  f = open(path, 'a')
  for text in texts:
    if not (isinstance(text, str) or isinstance(text, unicode)):
      #if isinstance(text, dict):
      text = copy.deepcopy(text)
      walk(text, func)
      text = str(text)
    f.write(text)
    f.write(' ')
  f.write('\n')
  f.close()

def matchDefinitonsAndCircumstances(AM, data, OR, true_bases):
  for feature in AM['feature']:
    if feature['POSpeech'] != data['POSpeech']: continue # так как могут быть и прилагательные, и притяж. местоимения.
    for descr_base in data['base']:
      #print 'matchDefinitonsAndCircumstances\n', feature['base'], descr_base
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
    write_log('00. Candidates for true bases:', AM)
    true_bases = matchArgument(OR, AM, Supplement, desc)
    write_log('01. True bases:', true_bases)
    _found_args[name] = list(set(true_bases))

  write_log('02. Found arguments: ', _found_args)
  # декартово умножение
  found_args = lingvo_math.dproduct(_found_args)
  # соответствие, если в предложении указано наречие "соответственно"
  # здесь должен быть этот код  
  write_log('02.1. Found arguments: ', found_args)
  return found_args

def checkArguments(found_args, argdesc, index_IL, ErrorConvert):
  # Проверяем аргументы на наличие в абстр. группе, заменяем по таблице и добавляем в ЯВ
  true_args = []
  #index = 0
  for found_arg in found_args:
    #true_args.append([])
    ErrorConvert.append([])
    for name, desc in argdesc.items():
      if 'int' in str(type(name)): continue
      if name not in found_arg:
        if desc['required']: ErrorConvert[-1].append("Required argument \"%s\" is absent!" % name)
        continue
      if desc['argtable']:
        if found_arg[name] in desc['argtable']: found_arg[name] = desc['argtable'][found_arg[name]]
        else: print u"Argument \"%s\" (found value \"%s\") is absent in argtable!" % (name, found_arg[name])
    true_args.append(found_arg)
    #true_args[index] = found_arg
    #index += 1
  write_log('03. True args:', true_args, '\n')
  return true_args
