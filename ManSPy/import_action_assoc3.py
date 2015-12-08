# -*- coding: utf-8 -*-
import LangModules, Action
import os, sys, re, pprint

NAME_LANG = r'[A-Z][a-z]+'
WORD = r'[a-zа-яёĉĝĥĵŝŭ]+'
WORD_WITH_PREPOSITION = '('+WORD+')?[ \t]*'+WORD

NAME_PYTHON_OBJ = r'[_a-zA-Z][_0-9a-zA-Z]*'
NAME_INTERNAL_OBJ = r'^\$'+NAME_PYTHON_OBJ
PATH_FUNCTION = NAME_PYTHON_OBJ+'/'+NAME_PYTHON_OBJ
ALL_NAMES_FUNCTION = r'^('+NAME_PYTHON_OBJ+'|'+NAME_INTERNAL_OBJ+')$'

# Парсинг Verbs
STRING_TITLE = ALL_NAMES_FUNCTION
STRING_BODY =  r'^ {4}'+NAME_LANG+'[ \t]*:[ \t]*'+WORD_WITH_PREPOSITION+'[ \t]*$'

# Парсинг WordCombination

STRING_DESTINATION_TITLE = r'^[_a-zA-Z0-9]+[ \t]*:[ \t]*'+PATH_FUNCTION+'[ \t]*$'
STRING_DESTINATION_BODY =  r'^ {4}'+NAME_LANG+'[ \t]*:[ \t]*'+WORD+'[ \t]*$'
STRING_ARGUMENT_TITLE1 = r'^'+NAME_PYTHON_OBJ+'[ \t]+[yn][ \t]*(;[ \t]*'+NAME_LANG+'[ \t]*)+$'
STRING_ARGUMENT_BODY = r'^ {4}[-_+a-zA-Z0-9а-яА-ЯёЁ]+[ \t]*(;[ \t]*('+WORD+')?[ \t]*)+$'
STRING_ARGUMENT_TITLE2 = r'^'+NAME_PYTHON_OBJ+'[ \t]+[yn][ \t]*$'
STRING_WCOMB_TITLE = r'^'+NAME_LANG+'$'
#STRING_WCOMB_ARGWORD = r'^ {4}'+WORD_WITH_PREPOSITION+'[ \t]*:[ \t]*'+WORD+'[ \t]*(,[ \t]*'+WORD+'[ \t]*)*$' # первое слово - предлог (иногда нужен)
STRING_WCOMB_ARGWORD = r'^ {4}('+WORD_WITH_PREPOSITION+'[ \t]*:[ \t]*'+WORD+'[ \t]*(,[ \t]*'+WORD+'[ \t]*)*;*)+$' # первое слово - предлог (иногда нужен)
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
  function = None
  verbs = {}
  for string in _fasif:
    if re.findall(STRING_TITLE.decode('utf-8'), string):
      function = string.strip()
    elif re.findall(STRING_BODY.decode('utf-8'), string):
      lang, verb = string.split(':')
      verbs[lang.strip()] = verb.strip()
  return {'function': function, 'verbs': verbs}

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

  arg_indexes = []
  arg_index = 0

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
    elif re.findall(STRING_ARGUMENT_TITLE1.decode('utf-8'), string):
      string = string.split(';')
      arg_name, isreq = string.pop(0).split()
      lang_indexes = []
      args[arg_name] = {'isreq': isreq, 'argtable': {}, 'argwords': {}}
      for lang in string:
        args[arg_name]['argtable'][lang.strip()] = {}
        lang_indexes.append(lang.strip())
      arg_indexes.append(arg_name)
      #print '3 $$$$', string
    # Аргумент ; АргументноеСловоНаЯзыке1 ; АргументноеСловоНаЯзыке2
    elif re.findall(STRING_ARGUMENT_BODY.decode('utf-8'), string):
      string = string.strip().split(';')
      arg_value = string.pop(0).strip()
      for index, word in enumerate(string):
        word = word.strip()
        if not word: continue
        args[arg_name]['argtable'][lang_indexes[index]][word] = arg_value
      #print '4 $$$$', string
    elif re.findall(STRING_ARGUMENT_TITLE2.decode('utf-8'), string):
      arg_name, isreq = string.split()
      args[arg_name] = {'isreq': isreq, 'argtable': {}, 'argwords': {}}
      arg_indexes.append(arg_name)
    ## Блок словосочетаний
    # Язык
    elif re.findall(STRING_WCOMB_TITLE.decode('utf-8'), string):
      lang = string.strip()
      for arg_name in args:
        args[arg_name]['argwords'][lang] = {'in_wcomb': {'name': None, 'hyperonyms': []}, 'another': []}
      arg_index = 0
      #print '5 $$$$', string
    # АргументноеСлово: АбстрактнаяГруппа1, АбстрактнаяГруппа2     Необходимо заменитиь на: # АргументноеСлово: ВходитАбстрГруппа1, ВходитАбстрГруппа2; НеВХодитАбстрГрупп, НеВХодитАбстрГрупп
    elif re.findall(STRING_WCOMB_ARGWORD.decode('utf-8'), string):
      arg_words = string.strip().split(';')
      #print arg_index, string
      arg_word, hyperonyms = arg_words.pop(0).split(':')
      args[arg_indexes[arg_index]]['argwords'][lang]['in_wcomb']['name'] = arg_word
      for hyperonym in hyperonyms.split(','):
        args[arg_indexes[arg_index]]['argwords'][lang]['in_wcomb']['hyperonyms'].append(hyperonym.strip())

      for _arg_word in arg_words:
        arg_word, hyperonyms = _arg_word.split(':')
        args[arg_indexes[arg_index]]['argwords'][lang]['another']['name'] = arg_word
        for hyperonym in hyperonyms.split(','):
          args[arg_indexes[arg_index]]['argwords'][lang]['another']['hyperonyms'].append(hyperonym.strip())
      arg_index += 1
      #print '6 $$$$', string
    elif re.findall(STRING_WCOMB.decode('utf-8'), string):
      wcomb[lang] = string.strip()
  return {'functions': functions, 'wcomb': wcomb, 'args': args}

def siftoutVerb(fasif, lang):
  verbs = fasif['verbs']
  if lang not in verbs: return None
  fasif['verbs'] = verbs[lang]
  return fasif

def siftoutWordCombination(fasif, lang):
  args = {}
  for arg_name, _args in fasif['args'].items():
    argtable = _args['argtable']
    if lang in argtable: _args['argtable'] = argtable[lang]
    elif not argtable: _args['argtable'] = {}
    else: return None
    argwords = _args['argwords']
    if lang in argwords: _args['argwords'] = argwords[lang]
    else: return None

  for destination, value in fasif['functions'].items():
    if lang in value['verbs']: value['verbs'] = value['verbs'][lang]
    elif not value['verbs']: continue
    else: return None

  if lang in fasif['wcomb']: fasif['wcomb'] = fasif['wcomb'][lang]
  else: return None

  return fasif

def get_dword(word, LangClass):
  return LangClass.NL2IL(word, ':postmorph')[0][0].getUnit('dict')[0]
def proccess_argword(argwords, LangClass):
  argwords['name'] = get_dword(argwords['name'], LangClass)
  for index, argword in enumerate(argwords['hyperonyms']):
    argwords['hyperonyms'][index] = get_dword(argword, LangClass)

def proccess_lingvo_dataVerb(fasif, LangClass, OR):
  fasif['verbs'] = get_dword(fasif['verbs'], LangClass)['base']
  return fasif

def proccess_lingvo_dataWordCombination(fasif, LangClass, OR):
  for arg_name, data in fasif['args'].items():
    #_data = {'argtable':{}}
    _data = data['argtable'].copy().items()
    for arg_word, argtable in _data:
      _arg_word = arg_word
      arg_word = get_dword(arg_word, LangClass)['base']
      del data['argtable'][_arg_word]
      data['argtable'][arg_word] = argtable
    #fasif['args'][arg_name] = _data

    proccess_argword(data['argwords']['in_wcomb'], LangClass)
    for argword in data['argwords']['another']:
      proccess_argword(argword, LangClass)

  for destination, value in fasif['functions'].items():
    if value['verbs']: value['verbs'] = get_dword(value['verbs'], LangClass)['base']

  fasif['wcomb'] = LangClass.NL2IL(fasif['wcomb'], ':synt')[0][0].getUnit('dict')

  return fasif

def selector_of_function(dict_assoc_types, _func_name, *func_args):
  for assoc_type, fasifs in dict_assoc_types.items():
    func_name = _func_name+assoc_type
    if func_name not in globals(): continue
    index = 0
    while index < len(fasifs):
      fasif = fasifs[index]
      new_fasif = globals()[func_name](fasif, *func_args)
      if not new_fasif: del dict_assoc_types[assoc_type][index]
      else:
        dict_assoc_types[assoc_type][index] = new_fasif
        index += 1
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
    # Отсеиваем ненужные языки
    dict_assoc_types = selector_of_function(dict_assoc_types, 'siftout', self.settings['language'])
    dict_assoc_types = selector_of_function(dict_assoc_types, 'proccess_lingvo_data', self.LangClass, self.OR)
    pprint.pprint(dict_assoc_types)


  def importAll(self):
    fasif_dir = os.path.join(os.path.dirname(__file__), 'Action')
    fasif_files = get_fasif_files(fasif_dir)
    for fasif_file in fasif_files: self.proccess(fasif_file, fasif_dir)
