# -*- coding: utf-8 -*-

import os

IFName = API = None

def init():
  file_auto = os.path.join(os.path.dirname(__file__), 'sentences.txt')
  if not os.path.exists(file_auto):
    f = open(file_auto, 'w')
    f.close()

  f = open(file_auto, 'r')
  sentences = f.read().split('\n')
  f.close()

  for sentence in sentences:
    if sentence and sentence[0] != '#':
      #print 'sentence:', sentence
      API.write_text(IFName, sentence)
      ra = range(API.getlen_text(IFName))
      for r in ra: API.read_text(IFName, 0)
  print 'completed :)'
