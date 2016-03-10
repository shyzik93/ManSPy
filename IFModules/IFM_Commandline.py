# -*- coding: utf-8 -*-
""" В скобках после ответа показано количество ответов, которое ИСУ вам покажет
    после нажатия на Enter, то есть при отправке пустого сообщения :)
"""
import time, os

IFName = API = None

def FromUser2():
  API.write_text(IFName, raw_input())

def run():
  while 1:
    API.write_text(IFName, raw_input())
    r_text = API.read_text(IFName, 0)
    if r_text: print r_text, '(%s)' % str(API.getlen_text(IFName))
    time.sleep(0.01)
