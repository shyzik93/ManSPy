#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib as u

def safe_image():
  file_name = 'I://photo.jpg'
  #fu = u.urlopen('http://192.168.0.100:8080/photo.jpg')
  fu = u.urlopen('http://spaces.ru')
  f = open(file_name, 'wb')
  f.write(fu.read())
  f.close()
  return file_name

# Команды, доступные из Интерактивной Системы управления (Interactive Management System)
def ListFuncIMS(ModuleSettings):
  argument_Esperanto = {}
  ListFunc = [
     {
      'func': safe_image,
      # для Эсперанто указываем корень глагола, для других ЕЯ - по-другому
      'Esperanto': {'verb': u'montr', 'noun': u'imag'}, # первый элемент - глагол (или список аналогов),
                             # второй - обстоятельство глагола, выраженное не наречием?
                             # т. к. обстоятельство, выраженное наречием, обрабатывается модулем логики. Там и задаётся вне зависимости от ЕЯ.
      'argument_Esperanto':argument_Esperanto,
      }
  ]
  return ListFunc
