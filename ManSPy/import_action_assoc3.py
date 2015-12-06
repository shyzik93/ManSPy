# -*- coding: utf-8 -*-
import LangModules, Action
import os, sys, re, pprint

NAME_LANG = r'[A-Z][a-z]+'
WORD = r'[a-zа-яёĉĝĥĵŝŭ]+'

STRING_DESTINATION_TITLE = r'^[_a-zA-Z0-9]+[ \t]*:[ \t]*[_a-zA-Z0-9]+/[_a-zA-Z0-9]+[ \t]*$'
STRING_DESTINATION_BODY =  r'^ {4}'+NAME_LANG+'[ \t]*:[ \t]*'+WORD+'[ \t]*$'
STRING_ARGUMENT_TITLE = r'^[_a-zA-Z0-9]+[ \t]+[yn][ \t]*(;[ \t]*'+NAME_LANG+'[ \t]*)+$'
STRING_ARGUMENT_BODY = r'^ {4}[-_+a-zA-Z0-9а-яА-ЯёЁ]+[ \t]*(;[ \t]*('+WORD+')?[ \t]*)+$'
STRING_WCOMB_TITLE = r'^'+NAME_LANG+'$'
STRING_WCOMB_ARGWORD = r'^ {4}('+WORD+')?[ \t]*'+WORD+'[ \t]*:[ \t]*'+WORD+'[ \t]*(,[ \t]*'+WORD+'[ \t]*)*$' # первое слово - предлог (иногда нужен)
STRING_WCOMB = r'^ {4}('+WORD+')?([ \t]+'+WORD+')*[ \t]*$' # Не должо совпадать с названием языка!

def get_fasif_files(modules_path):
  ''' Функция возвращает мимена МУ '''
  names = os.listdir(modules_path)
  #names [name for name in names if name[-4:]=='.fsf'] # короче, но требует дополнительную память

  x = 0 # длинее, но требует меньше памяти. Вероятно, медленней работаейт. Необходим замер времени
  while x < len(names):
    if names[x][-4:] != '.fsf': del names[x]
    else: x += 1
  return names

def separate_fasifs(fasif):
  fasif = re.sub(r"#[^:].*", '', fasif) # комментарии с середины строки
  #print fasif
  fasif = fasif.split('\n')
  version = fasif.pop(0) # для будущей совместимости версий, возможно.
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
  #pprint.pprint(dict_assoc_types)
  return dict_assoc_types

def parseVerb(_fasif):
  fasif = {'verbs': {}, 'function': _fasif.pop(0).strip()}
  for string in _fasif:
    lang, verb = string.split(':')
    fasif['verbs'][lang.strip()] = verb.strip()
  return fasif

def parseWordCombination(_fasif): # подформат состоит из трёх блоков: описание функций, аргументов и словосочетания. Аргументы одинаковы для всех функций
  functions = {}
  args = {}
  wcomb = {}

  ## Блок функций
  destination = None
  ## Блок аргументов
  arg_name = None
  lang_indexes = []
  ## Блок словосочетаний
  lang = None

  for string in _fasif:
    ## Блок функций
    # Назначение: Модуль/Функция
    if re.findall(STRING_DESTINATION_TITLE.decode('utf-8'), string): # "Name_01 : moduleName/funcName "
      destination, function = string.split(':')
      destination = destination.strip()
      functions[destination] = {'function': function.strip(), 'verbs': {}}
      #print '1 $$$$', string
    # Язык: глаголДляФункции
    elif re.findall(STRING_DESTINATION_BODY.decode('utf-8'), string): # "    Language : verbглагол"
      lang, verb = string.split(':')
      functions[destination]['verbs'][lang.strip()] = verb.strip()
      #print '2 $$$$', string
    ## Блок аргументов
    # аргумент yORn ; Язык1 ; Язык2
    elif re.findall(STRING_ARGUMENT_TITLE.decode('utf-8'), string):
      string = string.split(';')
      arg_name, isreq = string.pop(0).split()
      lang_indexes = []
      args[arg_name] = {}
      for lang in string:
        args[arg_name][lang.strip()] = {}
        lang_indexes.append(lang.strip())
      #print '3 $$$$', string
    # Аргумент ; АргументноеСловоНаЯзыке1 ; АргументноеСловоНаЯзыке2
    elif re.findall(STRING_ARGUMENT_BODY.decode('utf-8'), string):
      string = string.strip().split(';')
      arg_value = string.pop(0).strip()
      for index, word in enumerate(string):
        word = word.strip()
        if not word: continue
        args[arg_name][lang_indexes[index]][word] = arg_value
      #print '4 $$$$', string
    ## Блок словосочетаний
    # Язык
    elif re.findall(STRING_WCOMB_TITLE.decode('utf-8'), string):
      lang = string.strip()
      wcomb[lang] = {'argwords': {}}
      #print '5 $$$$', string
    # АргументноеСлово: АбстрактнаяГруппа1, АбстрактнаяГруппа2     Необходимо заменитиь на: # АргументноеСлово: ВходитАбстрГруппа1, ВходитАбстрГруппа2; НеВХодитАбстрГрупп, НеВХодитАбстрГрупп
    elif re.findall(STRING_WCOMB_ARGWORD.decode('utf-8'), string):
      arg_word, abstr_groups = string.strip().split(':')
      abstr_groups = abstr_groups.split(',')
      wcomb[lang]['argwords'][arg_word.strip()] = []
      for abstr_group in abstr_groups: wcomb[lang]['argwords'][arg_word.strip()].append(abstr_group.strip())
      #print '6 $$$$', string
    elif re.findall(STRING_WCOMB.decode('utf-8'), string):
      #print '7 $$$$', string
      wcomb[lang]['wcomb'] = string.strip()
  return {'functions': functions, 'wcomb': wcomb, 'args': args}

def proccess_lingvo_dataVerb(fasif, lang):
  return fasif

def proccess_lingvo_dataWordCombination(fasif, lang):
  return fasif

def selector_of_function(dict_assoc_types, func_name, *func_args):
  for assoc_type, fasifs in dict_assoc_types.items():
    func_name = func_name+assoc_type
    if func_name not in globals(): continue
    for index, fasif in enumerate(fasifs): dict_assoc_types[assoc_type][index] = globals()[func_name](fasif, *func_args)
  return dict_assoc_types

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
    if isinstance(fasif, str): fasif = fasif.decode('utf-8')
    dict_assoc_types = separate_fasifs(fasif)
    dict_assoc_types = selector_of_function(dict_assoc_types, 'parse')
    dict_assoc_types = selector_of_function(dict_assoc_types, 'proccess_lingvo_data', self.settings['language'])
    pprint.pprint(dict_assoc_types)

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
