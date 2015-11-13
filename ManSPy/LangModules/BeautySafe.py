# -*- coding: utf-8 -*-
''' Модуль вспомогательный. Сохраняет результаты анализов для последующего
    выявления ошибок и неточностей.
'''
import os, datetime, codecs
import common

'''db_dir = os.path.abspath('').split(os.path.sep)
db_dir.reverse() # нижний код для того, чторбы запускать файлы из любой нижней директории
for i in db_dir:
  if i == 'IMS':
    db_dir = db_dir[db_dir.index(i)+1:]
    break
db_dir.reverse()
db_dir[0] = db_dir[0] + os.sep
db_dir = os.path.join(*db_dir)
#db_dir = os.path.join(db_dir, 'DATA_BASE', 'log_analysis_')
print os.path.abspath('')
db_dir = os.path.join(os.path.abspath(''), 'log_analysis_')'''

def fwrite(data):
  #global db_dir
  db_dir = os.path.join(common.RSettings('dir_db'), 'analysis.txt')
  if not os.path.exists(db_dir):
    f = open(db_dir, 'w')
    f.close()
  with codecs.open(db_dir, 'a', 'utf-8') as f:
    f.write(data)#.decode('utf-8'))
    f.close()    

def safeResults(l, title, space=''):
  ''' удобно сохраняет список словарей или словарь словарей'''
  if title != None: fwrite(('- '*10)+title+(' -'*10)+u'\n')

  if str(type(l))[7:-2] == 'dict':
    l2 = []
    for k, v in l.items():
      l2.append(v)
    l = l2

  for res in l:
    if str(type(res))[7:-2] in ['int', 'str']:
      fwrite(space + str(res) + u'\n')
      continue
    for k, v in res.items():
      if str(type(v))[7:-2] == 'list':
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
  list_res = sentence.getSentence('dict')
  fwrite('----'+getTime()+'\n')

  sentence = ''
  for k, v in list_res.items(): sentence += v['word'] + ' '
  fwrite('Folding sentence: '+sentence+'\n')

  safeResults(list_res, title)

def safe_sentences(sentences, title):
  for sentence in sentences: safe_sentence(sentence, title)

def safe_IL(IL): fwrite('IL-sentence: '+str(IL)+'\n')
