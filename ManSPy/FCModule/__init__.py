# -*- coding: utf-8 -*-
''' Модуль-обёртка для интеллекта'''
from LogicKernel import LogicKernel
import HistoryIL, time

class LogicShell():
  def __init__(self, settings):
    self.settings = settings
    self.list_answers = {'general': []}
    self.LogicKernel = LogicKernel(self.list_answers)

  def Shell(self, IL, IFName):
    """ Обёртка функции интеллекта
    """
    # Обработка заданий
    if IL == None: return

    if IFName not in self.list_answers: self_list_answers[IFName] = []
    IL['arg0']['forread'] = self.list_answers[IFName]
    IL['arg0']['IFName'] = IFName
    self.LogicKernel.LogicKernel(IL)
