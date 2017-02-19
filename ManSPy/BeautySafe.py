# -*- coding: utf-8 -*-
''' Модуль вспомогательный. Сохраняет результаты анализов для последующего
    выявления ошибок и неточностей.
'''
import os, datetime
from pprint import pprint

def fwrite(data, name='analysis.txt'):
  if not os.path.exists(name):
    f = open(name, 'w')
    f.close()
  with open(name, 'a', encoding='utf-8') as f:
    f.write(data)
    f.close()    

def safeResults(l, title, space=''):
  ''' удобно сохраняет список словарей или словарь словарей'''
  if title != None: fwrite(('- '*10)+title+(' -'*10)+u'\n')

  if isinstance(l, dict):
    l2 = []
    for k, v in l.items():
      l2.append(v)
    l = l2

  for res in l:
    if isinstance(res, (int, str)):
      fwrite(space + str(res) + '\n')
      continue
    for k, v in res.items():
      if isinstance(v, list):
        fwrite(space + k + ' : \n')
        safeResults(v, None, space+'    ')
        continue
      fwrite(space + k + ' : ' + str(v) + '\n')
    index = l.index(res)
    if index != len(l)-1: fwrite('\n')

def safeUnknown(list_res):
  ''' запись нераспознанных слов ??????????'''
  l = []
  for res in list_res:
    #if res.has_key('POSpeech') == 0:
    #if len(res) == 1:
    if res['POSpeech'] == '':
      l.append(res['word'])
  index = 0
  while index < len(l):
    if l.count(l[index]) > 1: del l[index]
    index += 1
  t = ''
  for word in l: t += word + ' '
  fwrite(u'Нераспознанные слова: ' + t + u'\n\n')
  #f.close()

def getTime():
  now = datetime.datetime.now()
  return now.strftime("%Y.%m.%d %H:%M:%S")

# ---------------------------------------------------------------------

def safe_NL(NL): fwrite('NL-sentence: '+NL+'\n')

def safe_sentence(sentence, title):
  #print sentence.getUnit('str')
  list_res = sentence.getUnit('dict')
  #print list_res
  fwrite('----'+getTime()+'\n')
  fwrite('Folding sentence: '+str(sentence.getUnit('str'))+'\n')
  safeResults(list_res, title)

def safe_sentences(sentences, title):
  for index, sentence in sentences: safe_sentence(sentence, title)

def safe_IL(IL): fwrite('IL-sentence: '+str(IL)+'\n')
