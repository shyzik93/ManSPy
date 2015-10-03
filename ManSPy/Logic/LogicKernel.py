# -*- coding: utf-8 -*-
''' В модуле реализован логическтй аппарат ИСУ '''
import time, threading

class LogicKernel():
  def __init__(self, list_answers): self.list_answers = list_answers

  def call(self, func_obj, arg0, argument):
    res = func_obj(arg0, **argument)
    if res: self.list_answers[self.IFName].append(res)

  def RunFunc(self, arg0, subject, action, argument):
    """ Вызывает функцию, согласно обстоятелствам вызова """
    typecircumstance = ''
    circumstance = ''

    func_obj = action['function']
    if not callable(func_obj): # этотт д также добавить в import Action, чтобы фасиф не сохранялся с ошибкой
      print "Function \"%s\" is not callable!" % str(func_obj)
      return

    if action['type circumstance'] == 'speed':
      if action['circumstance'] == 'fast': pass
      elif action['circumstance'] == 'slow':
        print 'start'
        time.sleep(10)
        print 'stop'
    #self.list_answers[self.IFName].append(func_obj(arg0, **argument))
    self.call(func_obj, arg0, argument)

  def LogicKernel(self, IL, IFName):
    ''' Главная функция. Работает только с ВЯ '''
    self.IFName = IFName
    action = IL['action']
    subject = IL['subject']
    argument = IL['argument']
    arg0 = IL['arg0']

    if action['mood'] == 'imperative':
      # здесь можно проверить, кто дал приказ
      self.RunFunc(arg0, subject, action, argument)
    elif action['mood'] == 'indicative':
      # яв-предложение должно подаваться в функцию обработки фактов. А эта строчка - временная.
      self.RunFunc(arg0, subject, action, argument)

    if action['function'] == None: pass
