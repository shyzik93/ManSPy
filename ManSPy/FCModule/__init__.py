# -*- coding: utf-8 -*-
''' Модуль-обёртка для интеллекта'''
from LogicKernel import LogicKernel
import time

class BuiltInFunctions:
  def __init__(self, answers):
    self.answers = answers
  def ToUser(self, *results):
    self.answers.extend(results)

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
    self.LogicKernel = LogicKernel(self.list_answers)

  def Shell(self, IL, IFName):
    """ Обёртка функции интеллекта """
    # Обработка заданий
    if not IL: return
    if IFName not in self.list_answers: self.list_answers[IFName] = []

    bif = BuiltInFunctions(self.list_answers[IFName])
    common_func = IL['action']['common_verb_function']
    if isinstance(common_func, (str, unicode)):
      IL['action']['common_verb_function'] = getattr(bif, common_func) #locals()[common_func]

    IL['arg0']['forread'] = Message(self.list_answers[IFName])
    IL['arg0']['IFName'] = IFName
    self.LogicKernel.LogicKernel(IL)
