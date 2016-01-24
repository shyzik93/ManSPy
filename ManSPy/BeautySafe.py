# -*- coding: utf-8 -*-
''' Модуль вспомогательный. Сохраняет результаты анализов для последующего
    выявления ошибок и неточностей.
'''
import os, datetime, codecs
import common
from pprint import pprint

def fwrite(data, name='analysis.txt'):
  #global db_dir
  db_dir = os.path.join(common.RSettings('dir_db'), name)
  if not os.path.exists(db_dir):
    f = open(db_dir, 'w')
    f.close()
  with codecs.open(db_dir, 'a', 'utf-8') as f:
    f.write(data)#.decode('utf-8'))
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
      fwrite(space + str(res) + u'\n')
      continue
    for k, v in res.items():
      if isinstance(v, list):
        fwrite(space + k + u' : \n')
        safeResults(v, None, space+'    ')
        continue
      fwrite(space + k + ' : ' + unicode(v) + u'\n')
    index = l.index(res)
    if index != len(l)-1: fwrite(u'\n')

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
