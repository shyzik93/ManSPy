# -*- coding: utf-8 -*-
import os, shutil, re

def printOut(*args):
  _args = ''
  for arg in args: _args += arg + ' '
  print _args
main_path = os.path.dirname(__file__)

def deleteCash(rec=0, _path=None, names=None):
  if not rec:
    os.path.walk(main_path, deleteCash, 1)
    return
  for name in names:
    #print name[0] == '.', name
    #if name[0] == '.': continue
    path = os.path.join(_path, name)
    if os.path.isfile(path) and (path[-4:] == '.pyc' or path[-1] == '_'):
      printOut(path)
      os.remove(path)

#list_keys = ['POSpeech', 'MOSentence', 'category', 'feature', 'mood', 'tense', 'prefix']
#list_values = ['verb', 'noun', 'adverb', 'adjective', 'adnoun', 'direct supplement', 'supplement', 'predicate', 'subject', 'present', 'past', 'future', 'pronoun']
#list_values.extend(list_keys)
list_keys = ['POSpeech', 'MOSentence', 'category', 'feature', 'mood', 'tense', 'prefix', 'verb', 'noun', 'adverb',
             'adjective', 'adnoun', 'direct supplement', 'supplement', 'predicate', 'subject', 'present', 'past',
             'future', 'pronoun', 'preposition', 'conjunction', 'preposition_d', 'conjunction_d', 'case', 'number',
             'base', 'nominative', 'singular', 'class', 'ordinal', 'word', 'link', 'type', 'homogeneous_link',
             'antonym', 'action', 'argument', 'arg0', 'circumstance', 'type circumstance', 'function', 'possessive',
             'definition', 'definition', 'coordinating', 'subordinating', 'article', 'particle', 'infinitive',
             'imperative', 'indicative', 'subjunctive', 'end']

"""def edit_files(rec=0, _path=None, names=None):
  if not rec:
    os.path.walk(main_path+'_user', edit_files, 1)
    return
  for name in names:
    path = os.path.join(_path, name)  
    if os.path.isfile(path) and path[-3:] == '.py':
      f = open(path, 'r')
      text = f.read()
      f.close()
      #text = re.sub(r"\n#", '#', text)
      text = re.sub(r"\s*#.*", '', text)
      #text = re.sub(r"[^\\]#.*", '', text)
      for key in list_keys:
        text = re.sub(r"\[[\"\']"+key+r"[\"\']\]", '['+str(list_keys.index(key))+']', text)
      #for value in list_values:
      #  text = re.sub(r"u?[\"\']"+value+r"[\"\']", '\''+str(list_values.index(value))+'\'', text)
      for key in list_keys:
        text = re.sub(r"u?[\"\']"+key+r"[\"\']", str(list_keys.index(key)), text)
      f = open(path, 'w')
      f.write(u'# -*- coding: utf-8 -*-\n')
      f.write(text)
      f.close()"""

"""def make_user_version():
  user_path = main_path+'_user'
  orig_path = main_path
  # копируем
  if os.path.exists(user_path):
    shutil.rmtree(user_path)
  shutil.copytree(orig_path, user_path)
  # редактируем файлы (обфускация)
  edit_files()"""

#edit_files()
#make_user_version()
#deleteCash()

def olddeleteCash(start_path=main_path):
  """ Удаляет файлы:
      *.pyc - кеш Питона, *_ - логи ИСУ, которые можно удалять """
  names = os.listdir(start_path)
  new_paths = []
  # удаляем кеш, собираем в список найденные папки
  for name in names:
    ISM_name = start_path +"\\"+ name
    if os.path.isfile(ISM_name):
      if name[-4:] == '.pyc' or name[-1] == '_':
        os.remove(ISM_name)
    elif os.path.isdir(ISM_name):
      new_paths.append(name)

    # удаляем кеш во вложенных папках
    for path in new_paths:
      printOut(u'Удалён кеш в', start_path+"\\"+path)
      olddeleteCash(start_path +"\\"+ path)
