# -*- coding: utf-8 -*-
import LangModules, Action
import os, re

template = re.compile(r"[^_][a-zA-Z0-9_]+\.pyc?")

def _get_module_names(modules_path):
  ''' Функция возвращает мимена МУ '''
  names = os.listdir(modules_path)
  # удаляем файлы не модулей
  x = 0
  while x < len(names):
    if not re.match(template, names[x]):
      names.remove(names[x])
      x -= 1
    else:
      names[x] = names[x].split('.')[0]
    x += 1
  # Удаляем повторы
  for name in names:
    if names.count(name) == 2:
      names.remove(name)
  return names

def parse_assoccstring(assocstring):
  ''' Разбор строки ассоциации, то есть преобразует её в словарь.
      Формат строк: "АргСлово1: АбстрГруппа1 АбстрГруппа2; АргСлово2: АбстрГруппа1 # первый аргумент
                      АргСлово1: АбстрГруппа1 АбстрГруппа2; АргСлово2: АбстрГруппа1 № второй"
      Первое аргументное слово берётся из шаблона ЯЕ-предложения,
      следующие - произвольно, если аргументом будут слова из разных абст. групп.
      Парсер работает лишь с одной строкой!
  '''
  assoc = {}
  assocstring = assocstring.split(';')
  for assocsubstring in assocstring:
    assocsubstring = assocsubstring.strip().split(':')
    arg_word = assocsubstring[0].strip()
    word_groups = assocsubstring[1].split()
    assoc[arg_word] = word_groups
  return assoc

def parseFASIF(FASIF, language):
  ''' преобразует ФАСИФ-строку в ФАСИФ-словарь. '''
  language = language.capitalize()
  req_dict = {'y': True, 'n': False}
  if 'str' in str(type(FASIF)): FASIF = FASIF.decode('utf-8')
  
  fasif = {}
  FASIF = re.sub(r"\n#.*", '', FASIF) # комментарии с начала строки
  FASIF = re.sub(r"[^\\]#.*", '', FASIF) # комментарии с середины строки
  FASIFlangs = FASIF.strip().split('\n\n')
  FASIFfunc = FASIFlangs.pop(0).strip().split('\n')

  # Парсинг функционного блока
  fasif['func_name'] = FASIFfunc.pop(0)
  fasif['args'] = {}
  arg_name = None
  column = None
  args = [] #  для парсинга языкового блока
  for string in FASIFfunc:
    string = string.split(';')
    if string[0][:2] == '  ':
      # Парсинг таблицы жёстких ассоциаций
      base = string[column].strip()
      fasif['args'][arg_name]['table'][base] = string.pop(0).strip()
    else:
      # Парсинг заголовка подблока
      arg_name, required = string.pop(0).strip().split(' ')
      args.append(arg_name)
      for lang in string:
        if lang.strip().capitalize() == language:
          column = string.index(lang) + 1
          break
      fasif['args'][arg_name] = {}
      fasif['args'][arg_name]['required'] = req_dict[required]
      fasif['args'][arg_name]['table'] = {}

  # Парсинг языкового блока
  for FASIFlang in FASIFlangs:
    FASIFlang = FASIFlang.strip().split('\n')
    lang = FASIFlang.pop(0).capitalize()
    if lang != language: continue
    fasif['sentence'] = FASIFlang.pop()
    for string in FASIFlang:
      arg_name = args[FASIFlang.index(string)]
      fasif['args'][arg_name]['assoc'] = parse_assoccstring(string)
  if 'sentence' not in fasif:
    print 'FASIF wasn\'t found for %s language!' % language
    print FASIF
  return fasif

def proccess_lang_data(fasif, LangClass, R, module_name):
  ''' Обработка лингвистических данных: анализ, внесение в БД '''
  fasif['sentence'], GrammarNazi = LangClass.NL2IL(fasif['sentence'], ":synt")
  for arg_name in fasif['args']:
    assoc = fasif['args'][arg_name]['assoc']
    #print 'assoc:', assoc
    fasif['args'][arg_name]['assoc'] = []
    for word, groups in assoc.items():
      word = LangClass.NL2IL(word, ":postmorph")[0].GetSet(0)
      groups = [LangClass.NL2IL(group, ":morph")[0].GetSet(0)['base'] for group in groups]
      for group in groups:
        R.addWordsInAbstractGroup(group, word['base'])
        if fasif['args'][arg_name]['table']:
          R.addWordsInAbstractGroup(group, *fasif['args'][arg_name]['table'].keys())
      fasif['args'][arg_name]['assoc'].append([word] + groups)
      # Аргументные слова в таблице жёстких ассоциаций добавляются во все указанные абстрактные группы. Требуется дополнить ФАСИФ возможностью явного указания абстр. групп.
      #if fasif['args'][arg_name]['table']:
      #  OR.addWordsInAbstractGroup(word['base'], *fasif['args'][arg_name]['table'].keys())

#############################
def find_mediators(sentence, word, index, args, max_link_arg):
  parent_indexes = sentence.getControl(index)
  for parent_index in parent_indexes:
    parent_word = sentence.GetSet(parent_index)
    arg = {}
    if word.has_key('case'): arg['case'] = word['case']
    arg['MOSentence'] = word['MOSentence']
    arg['POSpeech'] = word['POSpeech']
    arg['base'] = word['base']
    arg['parentBase'] = parent_word['base'] # а здесь именно корень, а не список абстрактных групп
    arg['parentMOSentence'] = parent_word['MOSentence']
    arg['required'] = 1 # ???
    args[max_link_arg[0]] = arg
    max_link_arg[0] += 1
    if parent_word['MOSentence'] not in ['direct supplement', 'subject', 'predicate']:
      args[max_link_arg[0]-1]['parentLink'] = max_link_arg[0]
      find_mediators(sentence, parent_word, parent_index, args, max_link_arg)
    break # должно быть лишь одно управляющее слово, иначе невозможно определить, кто из них посредник.

def is_equal(word1, word2):
  # то есть слова должны совпадать вплоть до регистра букв
  if word1['word'] != word2['word']: pass
  # защита от одинакового слова с разными частями речи и корнями (например, для русского ЯЕ)
  elif word1['POSpeech'] != word2['POSpeech']: pass
  elif word1['base'] != word2['base']: pass
  else: return True
  return False

def make_args_descr(fasif, arg_name, args, max_link_arg):
  arg_dict = fasif['args'][arg_name]
  arg_word = arg_dict['assoc'][0] # остальные слова других абстр.групп нужно также добавить в хранимый ФАСИФ, а в конверторе анализов сделать код проверки.
  sentence = fasif['sentence']

  # извлекаем из предложения возможные слова-аргументы с их индексами в данном предложении
  if arg_word[0]['POSpeech'] in ['adjective', 'adverb']: # definition, circumstance
    _dict = sentence.getByCharacteristicFeatures('base', arg_word[0]['base'])
    dict_words = {}
    for parent_index, list_features in _dict.items():
      for feature in list_features:
        if is_equal(feature, arg_word[0]): dict_words[parent_index] = feature
  elif arg_word[0]['POSpeech'] == 'noun': # supplement, direct supplement, subject
    dict_words = sentence.getByCharacteristic('base', arg_word[0]['base'])
    for parent_index, word in dict_words.items():
      #print '    (ImportAction) word:', word
      #print '    arg_word[0]:', arg_word[0]
      #if not is_equal(word, arg_word[0]): dict_words[parent_index]
      if is_equal(word, arg_word[0]): dict_words[parent_index] = word
  else: return 1

  if len(dict_words) == 0: return 2
  parent_index, word = dict_words.items()[0] # выбираем первое слово-аргумент (повторы игнорируем)
  if len(dict_words) > 1: print "error4: word-argument is repeated in the sentence. Word-argument is \""+word['base']+"\""

  # определяем родителя и его индекс
  if word['MOSentence'] in ['definition', 'circumstance']:
    parent = sentence.GetSet(parent_index)
  else:
    parent_index = sentence.getControl(parent_index)
    if len(parent_index) > 1:
      print "error5: Word \""+word['word']+"\" has "+str(len(parent_index))+" parents. It's not right."
    elif len(parent_index) == 0:
      print "error6: Word \""+word['word']+"\" hasn't parents. It's not right."
      return 3
    parent_index = parent_index[0]
    parent = sentence.GetSet(parent_index)

  arg = {}
  if word.has_key('case'): arg['case'] = word['case']
  arg['MOSentence'] = word['MOSentence']
  arg['POSpeech'] = word['POSpeech']
  arg['base'] = arg_word[1:] # если список - то это абстрактные группы, как в данном случае.
  arg['required'] = arg_dict['required']
  arg['argtable'] = arg_dict['table']
  arg['parentBase'] = parent['base'] # а вот здесь именно корень, так как пока ещё мы не можем использовать переменного посредника или родителя
  arg['parentMOSentence'] = parent['MOSentence']
  if parent.has_key('case'): arg['parentCase'] = parent['case']
  #print 'Arguments before checking:', arg_name, arg
  #print '...and his parent:', parent['word'], parent
  if parent['MOSentence'] not in ['direct supplement', 'subject', 'predicate']:
    arg['parentLink'] = max_link_arg[0]
    find_mediators(sentence, parent, parent_index, args, max_link_arg)
  args[arg_name] = arg

def make_storedFASIF(fasif, module_name):
  ''' Создаёт хранимый ФАСИФ из словаря ФАСИФа '''
  storedFASIF = {
    'function': [module_name, fasif['func_name']],
    'arguments_description': {} }
  
  #indexes = range(len(fasif['args']))
  for arg_name in fasif['args'].keys():
    error = make_args_descr(fasif, arg_name, storedFASIF['arguments_description'], [0])
    if error != None: print "error in algorithm: code is", error
  return storedFASIF

def store_storedFASIF(fasif, storedFASIF, LangClass, OR):
  Subject, Predicate, DirectSupplement, Supplement, GrammarNazi, ErrorConvert = LangClass.NL2IL(fasif['sentence'], "extract")
  DS = DirectSupplement.values()
  if len(DS) == 0:
    print 'FASIF wasn\'t writen. Direct supplement is absent'
    return
  else: DS = DS[0]
  OR.procFASIF(Predicate.values()[0]['base'], DS['base'], storedFASIF)

class ImportAction():
  def __init__(self, settings):
    self.settings = settings
    self.OR = LangModules.ObjRelation.ObjRelation(settings['language'], settings['test'], settings['storage_version'])
    self.LangClass = LangModules.LangClass(settings, Action)

  def _import(self, module_name):
    ''' Импортирует МД, извлекает и преобразует ФАСИФ  словарь. '''
    list_FASIF = Action.getObject(module_name, 'list_FASIF')
    if list_FASIF == None: return
    for fasif in list_FASIF:
      fasif = parseFASIF(fasif, self.settings['language'])
      proccess_lang_data(fasif, self.LangClass, self.OR, module_name)
      storedFASIF = make_storedFASIF(fasif, module_name)
      store_storedFASIF(fasif, storedFASIF, self.LangClass, self.OR)
      #print '--------Import MA'
      #print fasif, '\n\n', storedFASIF
      #print '--------Import MA end'

  def importAll(self):
    module_names = _get_module_names(os.path.join(os.path.dirname(__file__), 'Action')) #Update
    for module_name in module_names: self._import(module_name)

if __name__ == '__main__':
  settings = {'language': 'Esperanto', 'test': True}

  MA = ImportAction(settings)
  MA._import('CurrencyLoader')
