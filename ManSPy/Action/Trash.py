#!/usr/bin/env python
# -*- coding: utf-8 -*-

def safe(file_name, text):
  f = open(file_name, 'w')
  f.write(text)
  f.close()
  return 'File saved successfully'

def Print():
  print 'You printed'
  return 'Printed'

# Команды, доступные из Интерактивной Системы управления (Interactive Management System)
def ListFuncIMS(ModuleSettings):
  argument_Esperanto = {0: [{}, False],
                        1: [{}, False] }
  ListFunc = [
    { 'func': safe,
      'Esperanto': {'verb': u'sav'},
      'argument_Esperanto': argument_Esperanto
      #'checking': {0: False, 1: False}
    }]

  ListFunc.append(
    { 'func': Print,
      'Esperanto': {'verb': 'print'},
      'argument_Esperanto': {}
    }
  )
  return ListFunc
