# -*- coding: utf-8 -*-
""" Модуль конвертирует результат морфологического синтаксического анализа
    предложения на ЕЯ Эсперанто во ВЯ
"""
#from IMS import Action
#from StartValue import circumstanceDict
import ObjRelation, processing_arguments
import copy

def get_values(dictionary, MOSentence, ErrorConvert):
  d = dictionary.values()
  if d: return d[0]
  else:
    ErrorConvert.append(MOSentence+' is absent!')
    return None

def get_procFASIFs(settings, Predicate, DirectSupplement, ErrorConvert):
  """ Извлекаем ФАСИФ, разбиваем его на список имён фукции и модуля,
      а также на словаврь описания аргументов."""

  # Вынимаем прямое дополнение (пока только одно)
  DS = get_values(DirectSupplement, 'Direct supplement', ErrorConvert)
  # Вынимаем сказуемое
  P = get_values(Predicate, 'Predicate', ErrorConvert)
  if not DS or not P: return {}

  # Находим ФАСИФ
  OR = ObjRelation.ObjRelation(settings['language'], settings['test'])
  procFASIF, isantonym = OR.procFASIF(P['base'], DS['base'])
  # если глагол является антонимом только по приставке или только по корню.
  if 'antonym' in P and P['antonym'] != isantonym: isantonym = True
  #print P['base'], DS['base']
  #print 'procFASIF:', procFASIF
  if procFASIF == None: ErrorConvert.append("FASIF for \""+P['word']+"\" and \""+DS['word']+"\" is absent")
  return [[procFASIF, isantonym]] # на случай нескольких прямых дополнений

def set_action(settings, Action, funcdesc, Predicate, IL):
  # Вынимаем функцию из ФАСИФа и добавляем её в ЯВ
  module_name, function_name = funcdesc
  module = Action.getModule(module_name)
  if 'settings' in dir(module): module.settings = settings # т. е. в МД  доступны настройки ИСУ
  if hasattr(module, function_name): IL['action']['function'] = getattr(module, function_name)
  else:
    print "Function \"%s\" is absent in module \"%s\". Function will not run!" % (module_name, function_name)
    print "You can rename the function in the module like in FASIF."
    IL['action']['function'] = None
  # заодно добавим и наклонение глагола
  IL['action']['mood'] = Predicate.values()[0]['mood']

def join_arg_and_func(true_arg, IL):
  _IL = copy.deepcopy(IL)
  #true_arg['arg0'] = arg0
  _IL['argument'] = true_arg
  return _IL

# если в предложении днесколько сказуемых или прямых дополнений, то оно должно
# разбиться на несколько предложений до вызова этой функции. То есть разбивка
# должна происходить в модуле, в котором эта функция вызывается. 
def Extraction2IL(settings, Action, Subject, Predicate, DirectSupplement, Supplement):
  pattern_IL = {
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
  OR = ObjRelation.ObjRelation(settings['language'])
  ErrorConvert = {'function': [], 'argument': []}
  procFASIFs = get_procFASIFs(settings, Predicate, DirectSupplement, ErrorConvert['function'])
  for procFASIF, isantonym in procFASIFs:
    if not procFASIF: continue
    IL = copy.deepcopy(pattern_IL) # на случай нескольких дополнений, так как это разные ЯВ будут
    funcdesc, argdesc = procFASIF['function'], procFASIF['arguments_description']#, procFASIF['arguments_order']
    found_args = processing_arguments.getArguments(OR, Subject, Predicate, DirectSupplement, Supplement, argdesc)
    true_args = processing_arguments.checkArguments(found_args, argdesc, len(ILs), ErrorConvert['argument'])

    IL['arg0']['antonym'] = isantonym
    set_action(settings, Action, funcdesc, Predicate, IL)
    ILs.extend([join_arg_and_func(true_arg, IL) for true_arg in true_args]) # на случай нескольких дополнений
  return ILs, ErrorConvert

# montru dolaran cambion de ukraina banko kaj de rusia banko
# В синтаксический модуль добавить поиск второго косвенного дополнения через просмотр однородности.

# montru euxran kaj dolaran cambion de ukraina kaj rusia banko - четыре числа
# montru euxran kaj dolaran cambion de ukraina kaj rusia banko соответсвенно - а тут уже два числа

#inkludu tablan lampon en dormĉambro kaj fermo
# {'device': '0', 'room': 'bedroom'}, 'subject': None}
# {'device': '0', 'room': u'ferm'}, 'error': ''}
