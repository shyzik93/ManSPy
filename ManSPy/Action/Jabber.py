#!/usr/bin/env python
# -*- coding: utf-8 -*-

bot = None
Settings = None

def go_offline():
  global bot
  bot.online = 0
  print 'going online by the command from user (it\'s not ERROR)'

# Команды, доступные из Интерактивной Системы управления (Interactive Management System)
def ListFuncIMS(ModuleSettings):
  global bot, Settings
  Settings = ModuleSettings
  bot = ModuleSettings['bot'] # для безопасности, ибо его тоже можно удалить из настроек (

  argument_Esperanto = {}
  ListFunc = [
    {
      'func': go_offline,
      'Esperanto': {'verb': u'blok'},
      'argument_Esperanto':argument_Esperanto
    }
  ]
  return ListFunc
