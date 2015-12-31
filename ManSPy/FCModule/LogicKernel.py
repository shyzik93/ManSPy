# -*- coding: utf-8 -*-
''' В модуле реализован логическтй аппарат ИСУ '''
import time, threading, sys

class LogicKernel():
  def __init__(self, list_answers): self.list_answers = list_answers

  def _call(self, func_obj, arg0, arguments):
    # Внутри функции можно писать в arg0['forread'], а можно просто возвратить.
    for argument in arguments:
      res = func_obj(arg0, **argument)
      if res or res==0: self.list_answers[arg0['IFName']].append(res)

  def RunFunc(self, arg0, subject, action, arguments):
    """ Вызывает функцию, согласно обстоятелствам вызова """

    #func_obj = action['wcomb_function']
    #if not callable(func_obj): # этот также добавить в import Action, чтобы фасиф не сохранялся с ошибкой
    #  sys.stderr.write("Function \"%s\" is not callable!" % str(func_obj))
    #  return

    #self._call(func_obj, arg0, argument)

    if action['wcomb_verb_function'] is not None:
      for argument in arguments:
        res = action['wcomb_verb_function'](arg0, **argument)
        if res or res==0: self.list_answers[arg0['IFName']].append(res)
      #self._call(action['wcomb_verb_function'], arg0, arguments)
    else:
      for argument in arguments:
        res = action['wcomb_function'](arg0, **argument)
        if res or res==0: action['common_verb_function'](res)

    #typecircumstance = ''
    #circumstance = ''

    #if action['type circumstance'] == 'speed':
    #  if action['circumstance'] == 'fast': pass
    #  elif action['circumstance'] == 'slow':
    #    print 'start'
    #    time.sleep(10)
    #    print 'stop'
    #self.list_answers[self.IFName].append(func_obj(arg0, **argument))

  def LogicKernel(self, IL):
    ''' Главная функция. Работает только с ВЯ '''
    action = IL['action']
    subject = IL['subject']
    arguments = IL['argument']
    arg0 = IL['arg0']

    if action['mood'] == 'imperative':
      # здесь можно проверить, кто дал приказ
      self.RunFunc(arg0, subject, action, arguments)
    elif action['mood'] == 'indicative':
      # яв-предложение должно подаваться в функцию обработки фактов. А эта строчка - временная.
      self.RunFunc(arg0, subject, action, arguments)
