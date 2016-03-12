# -*- coding: utf-8 -*-

import os, json, re

IFName = API = None


def init(settings=None):
  if not settings: settings = {'write_origin': True, 'compare_with_origin': False}
  #if not settings: settings = {'write_origin': False, 'compare_with_origin': True}
  file_auto = os.path.join(os.path.dirname(__file__), 'autofeed_sentences.txt')
  if not os.path.exists(file_auto):
    f = open(file_auto, 'w')
    f.close()

  f = open(file_auto, 'r')
  sentences = re.split("\n\r?", f.read())
  f.close()

  if settings['compare_with_origin']:
    f = open('autofeed_origin.txt', 'r')
    origin = json.load(f)
    f.close()
    res = open('autofeed_results.txt', 'w')
  elif settings['write_origin']: origin = {}

  gen_res = True
  for sentence in sentences:
    if not sentence or sentence[0] == '#': continue
    if settings['compare_with_origin']: res.write(sentence+'\n')
    if settings['write_origin']: origin[sentence] = []
    API.write_text(IFName, sentence)
    ra = range(API.getlen_text(IFName))
    for r in ra:
      r_text = API.read_text(IFName, 0)
      if settings['compare_with_origin']:
        if sentence in origin:
          if r_text in origin[sentence]: res.write('    True >>> ')
          else:
            gen_res = False
            res.write('    False >>> ')
        else: res.write('    sentence is absent >>> ')
        res.write(r_text+'\n')
      elif settings['write_origin']: origin[sentence].append(r_text)

  if settings['compare_with_origin']:
    res.write(str(gen_res)+'\n')
    res.close()
  elif settings['write_origin']:
    f = open('autofeed_origin.txt', 'w')
    f.write(json.dumps(origin))
    f.close()

  print 'completed :)'
