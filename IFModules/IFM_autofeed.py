# -*- coding: utf-8 -*-

import os, json, re, os

IFName = API = None

file_name_origin = 'autofeed_origin.txt'
file_name_guess = 'autofeed_results.txt'
file_name_sentences = 'autofeed_sentences.txt'

def init(settings=None):
  if not settings: settings = {'write_origin': False, 'compare_with_origin': True}
  if not os.path.exists(file_name_origin): settings = {'write_origin': True, 'compare_with_origin': False}
  #if not settings: settings = {'write_origin': False, 'compare_with_origin': True}
  file_auto = os.path.join(os.path.dirname(__file__), file_name_sentences)
  if not os.path.exists(file_auto):
    f = open(file_auto, 'w')
    f.close()

  if settings['compare_with_origin']:
    f = open(file_name_origin, 'r')
    origin = json.load(f)
    f.close()
    res = open(file_name_guess, 'w')
  elif settings['write_origin']: origin = {}

  gen_res = True
  with open(file_auto, 'r') as file_sentences:
    for sentence in file_sentences:
      sentence = sentence.strip()
      if not sentence or sentence[0] == '#': continue
      if settings['compare_with_origin']: res.write(sentence+'\n')
      if settings['write_origin']: origin[sentence] = []
      API.write_text(IFName, sentence)
      ra = range(API.getlen_text(IFName))
      for r in ra:
        r_text = API.read_text(IFName, 0)
        if settings['compare_with_origin']:
          if sentence in origin:
            if r_text in origin[sentence]: res.write('    True >>> '+r_text+'\n')
            else:
              gen_res = False
              res.write('    False >>> '+r_text+'\n')
              res.write('        ORIGINS: '+str(origin[sentence])+'\n')
          else: res.write('    sentence is absent >>> '+r_text+'\n')
        elif settings['write_origin']: origin[sentence].append(r_text)

  if settings['compare_with_origin']:
    res.write(str(gen_res)+'\n')
    res.close()
  elif settings['write_origin']:
    f = open(file_name_origin, 'w')
    f.write(json.dumps(origin))
    f.close()

  print('completed :)')
