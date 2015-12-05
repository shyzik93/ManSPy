# -*- coding: utf-8 -*-
import LangModules, Action
import os, sys, re, pprint

def get_fasif_files(modules_path):
  ''' Функция возвращает мимена МУ '''
  names = os.listdir(modules_path)
  #names [name for name in names if name[-4:]=='.fsf'] # короче, но требует дополнительную память

  x = 0 # длинее, но требует меньше памяти. Вероятно, медленней работаейт. Необходим замер времени
  while x < len(names):
    if names[x][-4:] != '.fsf': del names[x]
    else: x += 1
  return names

def parseFASIF(fasif, language):
  fasif = re.sub(r"#[^:].*", '', fasif) # комментарии с середины строки
  print fasif
  fasif = fasif.split('\n')
  dict_assoc_types = {}
  assoc_type = None
  for string in fasif:
    string = string.rstrip()
    if not string: continue
    if len(string) > 2 and string[:2] == '#:':
      assoc_type = string[2:]
      if assoc_type not in dict_assoc_types: dict_assoc_types[assoc_type] = []
      dict_assoc_types[assoc_type].append([])
      continue
    dict_assoc_types[assoc_type][-1].append(string)
  pprint.pprint(dict_assoc_types)
  return fasif

class ImportAction(object):
  def __init__(self, settings):
    self.settings = settings
    self.OR = LangModules.relation.ObjRelation(settings['language'], settings['test'], settings['storage_version'])
    self.LangClass = LangModules.LangClass(settings, Action)

  def proccess(self, fasif_file, fasif_dir):
    ''' Импортирует МД, извлекает и преобразует ФАСИФ  словарь. '''
    #list_FASIF = Action.getObject(module_name, 'list_FASIF')
    with open(os.path.join(fasif_dir, fasif_file)) as f:
      fasif = f.read()
    fasif = parseFASIF(fasif, self.settings['language'])

    #proccess_lang_data(fasif, self.LangClass, self.OR, module_name)
    #storedFASIF = make_storedFASIF(fasif, module_name)
    #store_storedFASIF(fasif, storedFASIF, self.LangClass, self.OR)
    #print '--------Import MA'
    #print fasif, '\n\n', storedFASIF
    #print '--------Import MA end'

  def importAll(self):
    fasif_dir = os.path.join(os.path.dirname(__file__), 'Action')
    fasif_files = get_fasif_files(fasif_dir)
    for fasif_file in fasif_files: self.proccess(fasif_file, fasif_dir)
