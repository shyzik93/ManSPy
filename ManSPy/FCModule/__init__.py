# -*- coding: utf-8 -*-
''' Модуль-обёртка для интеллекта'''
from .LogicKernel import LogicKernel
import time

'''class BuiltInFunctions:
  def __init__(self, answers):
    self.answers = answers
  def ToUser(self, *results):
    self.answers.extend(results)'''

class Message:
  ''' Для работы с результатами, возвращаемыми функциями действий '''
  def __init__(self, answers):
    self.answers = answers

  def add2read(self, r_text):
    # здесь можно конвертировать ответ на естественный язык...
    self.answers.append(r_text)

class LogicShell:
  def __init__(self, settings):
    self.settings = settings
    self.list_answers = {'general': []}
    self.reses = {}
    self.LogicKernel = LogicKernel(self.list_answers, self.reses)

  def Shell(self, IL, IFName):
    """ Обёртка функции интеллекта """
    # Обработка заданий
    if not IL: return
    if IFName not in self.list_answers: self.list_answers[IFName] = []

    '''bif = BuiltInFunctions(self.list_answers[IFName])
    common_func = IL['action']['common_verb_function']
    if isinstance(common_func, (str, unicode)):
      IL['action']['common_verb_function'] = getattr(bif, common_func) #locals()[common_func]'''

    IL['arg0']['forread'] = Message(self.list_answers[IFName])
    IL['arg0']['IFName'] = IFName
    self.LogicKernel.LogicKernel(IL)

  def execIL(self, _ILs, _ErrorConvert, IFName):
    ExecError = []
    if _ErrorConvert['function']: return ExecError
    #print(_ILs)

    index = 0
    for index_sentence, ILs in _ILs.items():
      self.reses[IFName] = []
      #print(ILs)
      for IL in ILs:
        action = IL['action']
        arg0 = IL['arg0']
        if not _ErrorConvert['argument'][index]: self.Shell(IL, IFName)
        index += 1
        if action['wcomb_verb_function'] is None:
          res = action['common_verb_function'](arg0, *self.reses[IFName])
          if res or res==0: self.list_answers[IFName].append(res)
        
    return ExecError
