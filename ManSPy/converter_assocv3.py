# -*- coding: utf-8 -*-

import to_formule, NLModules

def Extraction2IL(OR, settings, Action, predicates, arguments):
  #print '    predficates ::', predicates, '\n'
  #print '    arguments ::', arguments, '\n'

  fdb = to_formule.FasifDB(settings)

  # Вынимаем Фасиф
  x = 0
  for _argument in arguments:
    #argument = NLModules.ObjUnit.Sentence([])
    #argument.dict_unit = _argument
    argument = NLModules.ObjUnit.Sentence(_argument)
    print x, argument.getUnit('str')['fwords']
    #argument = argument.getUnit('dict')

    finded_args, fasifs = fdb.getFASIF('WordCombination', argument)
    print  finded_args, fasifs
    #fwcomb = to_formule.to_formule(argument, False)
    #print x, fdb.get_hashWComb(fwcomb)
    x += 1
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
