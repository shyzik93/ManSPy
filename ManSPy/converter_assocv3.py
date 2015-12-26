# -*- coding: utf-8 -*-

import codecs
import to_formule, NLModules, mymath

def check_args(finded_args, fasif, R):
  # Проверка на наличие в абстрактной группе
  hyperonyms = {}
  for argname, data in fasif['argdescr'].items():
    # пока только основные гиперонимы вытягиваем
    hyperonyms[argname] = [word['base'] for word in data['hyperonyms']]
  for finded_arg in finded_args:
    for argname, argvalue in finded_arg.items():
      isright = False
      for hyperonym in hyperonyms[argname]:
        if R.isWordInAbstractGroup(argvalue, hyperonym):
          isright = True
          break
      if not isright: del finded_arg[argname]
  # Проверка на отсутствие обязательных аргументных слов
  checked_args = []
  for finded_arg in finded_args:
    isright = True
    for argname, argdescr in fasif['argdescr'].items():
      if argname not in finded_arg and argdescr['isreq']: # если отсутствует обязательный аргумент
        isright = False
        break
    if isright: checked_args.append(finded_arg)

  return checked_args

def Extraction2IL(R, settings, Action, predicates, arguments):
  #print '    predficates ::', predicates, '\n'
  #print '    arguments ::', arguments, '\n'

  fdb = to_formule.FasifDB(settings)

  # Вынимаем Фасиф
  for _argument in arguments:
    argument = NLModules.ObjUnit.Sentence(_argument)
    compared_fasifs = fdb.getFASIF('WordCombination', argument)
    for id_fasif, data in compared_fasifs.items():
      finded_args, fasif = data
      for argname, args in finded_args.items(): finded_args[argname] = list(set(args))
      finded_args = mymath.dproduct(finded_args)
      finded_args = check_args(finded_args, fasif, R)
      compared_fasifs[id_fasif] = (finded_args, fasif)
      with codecs.open('comparing_fasif.txt', 'a', 'utf-8') as flog:
        flog.write('\n%s\n%s\n' % (str(finded_args), str(fasif['functions'])))
      
    #fwcomb = to_formule.to_formule(argument, False)
    #print x, fdb.get_hashWComb(fwcomb)
  print 

  # Составляем слооварь аргументов
  # Определяем функции и сотавляем ВЯ.

  '''pattern_IL = {
    'arg0': {'antonym': False}, # передаётся первым аргументом в каждую функцию
    'action': {
      'function': None,
      'mood': '',
      'circumstance': '',
      'type circumstance': ''
      },
    'argument': {},
    'subject': None
  }
  ILs = []
  ErrorConvert = {'function': [], 'argument': []}
  #procFASIFs = {}
  #for indexDS, DS in DirectSupplement.items():
  #  procFASIFs[indexDS] = get_procFASIFs(OR, settings, Predicate, DS, ErrorConvert['function'])
  procFASIFs = get_procFASIFs(OR, settings, Predicate, DirectSupplement, ErrorConvert['function'])
  for procFASIF, isantonym in procFASIFs:
    #procFASIF, isantonym = _procFASIF
    if not procFASIF: continue
    IL = copy.deepcopy(pattern_IL) # на случай нескольких дополнений, так как это разные ЯВ будут
    funcdesc, argdesc = procFASIF['function'], procFASIF['arguments_description']#, procFASIF['arguments_order']
    found_args = processing_arguments.getArguments(OR, Subject, Predicate, DirectSupplement, Supplement, argdesc)
    true_args = processing_arguments.checkArguments(found_args, argdesc, len(ILs), ErrorConvert['argument'])

    IL['arg0']['antonym'] = isantonym
    set_action(settings, Action, funcdesc, Predicate, IL)
    ILs.extend([join_arg_and_func(true_arg, IL) for true_arg in true_args]) # на случай нескольких дополнений
  return ILs, ErrorConvert'''
  return [], {'function': [], 'argument': []}
