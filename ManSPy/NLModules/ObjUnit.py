# -*- coding: utf-8 -*-
# Author: Ra93POL
# Date: 2.12.2014 - nowdays
import copy, re

class _Unit(object):
  ''' unit(index) - извлечение подъюнита
      unit(index, name) - извлечение характеристики подъюнита
      unit(index, name, value) - изменение характеристики подъюнита
      unit[name] - извлечение характеристики юнита
      unit[name] = value - изменение характеристики юнита
      name in unit - проверка наличия ключа характеристики юнита
      len(unit) - извлечение длины юнита

      Юнит - это предложение или слово. Подъюнит - их составляющие:
      для предложения - это слова, для слов - это символы'''

  def _update_added_unit(self, subunit): pass

  def _init(self, unit_info=None, dict_unit=None, properties_with_indexes=None):
    self.unit_info = unit_info or {}
    self.dict_unit = dict_unit or {}
    self.full_info = {'unit_info': self.unit_info, 'unit': self.dict_unit}

    self.properties_with_indexes = properties_with_indexes or []

    self.position = 0
    self.keys = self.dict_unit.keys()

  # Работа с информацией о юните в целом
  def __setitem__(self, key, value): self.unit_info[key] = value
  def __getitem__(self, key): return self.unit_info[key]
  def __delitem__(self, key): del self.unit_info[key]
  def __contains__(self, name): return name in self.unit_info

  #def __repr__(self): return self.__class__.__name__ + "(" + str(self.full_info) + ")"
  def __repr__(self): return self.__class__.__name__ + "(" + str(self.unit_info) + ")"
  def items(self): return self.dict_unit.items() # аналогично itemsUnit() без индекса. Не рекомендуется. Только для внутреннего использования.
  def itemsInfo(self): return self.unit_info.items()
  def itemsUnit(self, index=None):
    return self.dict_unit.items() if index == None else self.dict_unit[index].items()
  def update(self, _dict): self.unit_info.update(_dict)

  # Работа с информацией о составляющих юнит (подюнитов)
  def __len__(self): return len(self.dict_unit)
  def __call__(self, index, name=None, value=None): # типа getByIndex()
    if name == None: return self.dict_unit[index]
    elif value == None: return self.dict_unit[index][name]
    self.dict_unit[index][name] = value

  # Итератор
  def __iter__(self, position=0): # # аналогично itemsUnit() без индекса, но с возможностью управления текущей позицией. Для цикла for.
    self.position = position
    self.keys = self.dict_unit.keys()
    while self.position < len(self.keys) and self.position >= 0:
      index = self.keys[self.position]
      yield index, self.dict_unit[index]
      self.position += 1
    self.position = 0
  def iterFromByStep(self, step=0):
    position = self.position+step if step!=None else 0
    return self.__iter__(position)
  def iterFromByIndex(self, index):
    position = self.keys.index(index)
    return self.__iter__(position)
  def jumpByStep(self, step=1): self.position += step # аналог next() 
  def jumpByIndex(self, index): self.position = self.keys.index(index)
  def delByStep(self, count=1, step=0, jump_step=-1):
    for c in range(count): del self.dict_unit[self.keys[self.position+step]]
    self.keys = self.dict_unit.keys()
    self.position += jump_step
  def delByPos(self, position):
    del self.dict_unit[self.keys[position]]
    self.keys = self.dict_unit.keys()
  def delByIndex(self, *indexes):
    for index in indexes: del self.dict_unit[index]
    self.keys = self.dict_unit.keys()
  def getByStep(self, step=0, name=None, value=None):
    return self.__call__(self.keys[self.position+step], name, value)
  def getByPos(self, position, name=None, value=None):
    return self.__call__(self.keys[position], name, value)
    #return self.dict_unit[self.keys[position]]
  def currentIndex(self,step=0):return self.keys[self.position+step] # derpricated

  def isOutLeft(self, step=0):  return self.position+step <  0
  def isFirst(self, step=0):    return self.position+step == 0
  def isBetween(self, step=0):  return self.position+step <  len(self.dict_unit) - 1 and self.position+step > 0
  def isLast(self, step=0):     return self.position+step == len(self.dict_unit) - 1
  def isOutRight(self, step=0): return self.position+step >  len(self.dict_unit) - 1
  def isEntry(self, step=0):    return self.position+step >= 0 and self.position+step < len(self.dict_unit)

  def getNeighbours(self, step=0):
    left = self.dict_unit[self.keys[self.position+step-1]] if self.position != 0 else None
    right = self.dict_unit[self.keys[self.position+step+1]] if self.position != len(self.keys)-1 else None
    return left, right
  '''def isUnit(self, in_relpos, step=0):
    relpos = None# relatiove position
    pos = self.position + step
    maxpos = len(self.dict_unit)-1
    if pos < 0: relpos = 'left'
    elif pos == 0: relpos = 'first'
    elif pos < maxpos: relpos = 'between'
    elif pos == maxpos: relpos = 'last'
    elif pos > maxpos: relpos = 'right'
    relpos2 = 'belong' if relpos in ('first', 'between', 'last') else None
    return relpos in in_relpos.split() or relpos2 in in_relpos.split()'''

  # Прочее
  def getLen(self, func=None):
    """ Возвращает длину юнита (кол-во подюнитов). Может применить к длине функцию,
        например range, после этого возвратится список """
    return func(len(self.dict_unit)) if func else len(self.dict_unit)

  def _go_depth(self, el, info0, info1, info2):
    if isinstance(el, Sentence): return el.getUnit('dict', info0, info1, info2)
    elif isinstance(el, Word): return el.getUnit('dict', info0, info1, info2)
    elif isinstance(el, dict):
      _el = {}
      for k, v in el.items(): _el[k] = self._go_depth(v, info0, info1, info2)
      return _el
    elif isinstance(el, list):
      _el = []
      for v in el: _el.append(self._go_depth(v, info0, info1, info2))
      return _el
    else: return el

  def getUnit(self, Type, info0='members', info1='members', info2='info'):
    info = {'Text':info0, 'Sentence': info1, 'Word': info2}[self.__class__.__name__]
    if Type == 'dict':
      if info == 'info': dct = self.unit_info
      elif info == 'members': dct = self.dict_unit
      elif info == 'full': dct = self.full_info
      else:
        print "the argument '%s' of Unit.getUint is wrong!" % info
        return
      dct = copy.deepcopy(dct)
      return self._go_depth(dct, info0, info1, info2)
    elif Type == 'listSubUnits': # возвращает список подюнитв
      l = len(self.dict_unit)
      listDict = []
      for index in range(l): listDict.append(self.dict_unit[index])
      return listDict
    elif Type == 'str' and isinstance(self, Sentence): # Только для предложений!!!
      str_s = {'words': '', 'bases': '', 'fwords': '', 'fbases': ''}
      for index, sunit in self.dict_unit.items():
        str_s['words'] += ' ' + sunit['word']
        if 'base' in sunit: str_s['bases'] += ' ' + sunit['base']
        if 'feature' in sunit: 
          for feature in sunit['feature']:
            str_s['fwords'] += ' ' + feature['word']
            if 'base' in sunit: str_s['fbases'] += ' ' + feature['base']
        str_s['fwords'] += ' ' + sunit['word']
        if 'base' in sunit: str_s['fbases'] += ' ' + sunit['base']
      return str_s
    elif Type == 'str' and isinstance(self, word):
      str_s = ''
      for index, sunit in self.dict_unit.items():
        str_s += sunit['symbol']
      return str_s

  def _parseSettingsString(self, setstring):
    ''' Функция обработки строки настройки функции массовой обработки подъюнитов
       Пример строки:
       "subiv:ignore" - обрабатывать юниты как обычно.
       "subiv:noignore-feature" - обрабатывать юниты как обычно, но ещё и в значениях с ключом feature.
       "subiv:noignore-^feature" - обрабатывать юниты как обычно, но ещё и во всех значениях, кроме ключа feature.
       "subiv:only-feature" - обрабатывать юниты только в значениях с ключом feature.
       "subiv:only-^feature" - обрабатывать юниты только в значениях, кроме ключа feature.
       "list:eq" - списки, кортежи и словари сравнивать.
       "list:in" - проверять вхождение значений в список, кортеж и словарь. '''
    setdict = {'list': {'setvalue':'in', 'negative':False, 'names':[]},
                     'subiv': {'setvalue':'ignore', 'negative':False, 'names':[]}, }
    setstring = re.split(r' *; *', setstring.lower())
    for _setstring in setstring:
      #print setstring, re.findall(r'([a-z]+) *: *([a-z]+) *(?:- *(\^[a-z]+(?: *, *[a-z]+)?))?', _setstring)
      if not _setstring: continue
      setname, setvalue, names = re.findall(r'([a-z]+) *: *([a-z]+) *(?:- *(\^[a-z]+(?: *, *[a-z]+)?))?', _setstring)[0]
      negative = False if not names or names[0] != '^' else True
      names = names[1:] if negative else names
      names = re.split(r' *, *', names)
      names = [] if not names[0] else names
      setdict[setname] = {'setvalue':setvalue, 'negative':negative, 'names':names}
    #print 'setdict:', setdict
    return setdict

  # Коллекция функций для массовой работы с подъюнитами, имеющих одинаковые значения свойств.
  def _compare_subunit(self, subunit, properties, setdict):
    counter = len(properties)
    for name, value in properties.items():
      if not isinstance(value, tuple): value = (value,)
      if isinstance(value[0], (list, tuple, dict)) and setdict['setvalue'] == 'in':
        if name not in subunit: continue
        _counter = len(value)
        for _value in value:
          if _value in subunit[name]: _counter -= 1
        if not _counter: counter -= 1
      else:
        if name in subunit and subunit[name] in value: counter -= 1
        #if 'index' in subunit: print '  ;;;;', subunit['word'], counter
    if not counter: return True

  def _compare_subunits_in_values(self, subunit, properties, setdict):
    _subunits = []
    for name, value in subunit.itemsInfo():
      if not isinstance(value, list): continue
      for _subunit in value:
        #print '  ;;;;', subunit['word'], _subunit['word'], isinstance(_subunit, type(subunit))
        if not isinstance(_subunit, type(subunit)): continue
        if self._compare_subunit(_subunit, properties, setdict): _subunits.append(_subunit)
    #print '     ---subunits: ', _subunits
    return _subunits

  def getByValues(self, setstring='', **properties):
    ''' Возвращает слова, имеющие одниаковые значения свойств properties '''
    setdict = self._parseSettingsString(setstring)
    for index, subunit in self.dict_unit.items():
      _subunits = []
      if setdict['subiv']['setvalue'] in ('noignore', 'only'):
        _subunits = self._compare_subunits_in_values(subunit, properties, setdict)
        if setdict['subiv']['setvalue'] == 'only' and _subunits:
          yield index, None, _subunits
          continue
      if self._compare_subunit(subunit, properties, setdict):
        yield index, subunit, _subunits
      else:
        if _subunits: yield index, None, _subunits
  def changeByValues(self, name, value, setstring='', **properties):
    ''' Устанавлвает значение value свойства name слов, имеющих одниаковые значения свойств properties '''
    for index, subunit, _subunits in self.getByValues(setstring, **properties):
      for _subunit in _subunits: _subunit[name] = value
      if subunit: subunit[name] = value
  def chmanyByValues(self, new_properties, setstring='', **properties):
    ''' Устанавлвает значения свойств new_prperties слов, имеющих одниаковые значения свойств **properties '''
    for index, subunit, _subunits in self.getByValues(setstring, **properties):
      #print '     subunit:', subunit
      #print '     _subunits:', _subunits
      for _subunit in _subunits: _subunit.update(new_properties)
      if subunit: subunit.update(new_properties)

  def append(self, subunit):
    indexes = []
    for _subunit in self.dict_unit.values():
      for key, value in _subunit.items():
        if key in self.properties_with_indexes: indexes.append(value)
    indexes.extend(self.dict_unit.keys())

    max_index = max(indexes)+1 if indexes else 0
    self._update_added_unit(subunit)
    self.dict_unit[max_index] = subunit
    self.keys = self.dict_unit.keys()

  def pop(self):
    pass

class Word(_Unit):
  """ Класс объекта слова.
      При инициализации класса ему передаётся слово в виде строки. """  
  def __init__(self, str_word):
    self.str_word = str_word
    self._init(unit_info={'word': self.str_word, 'symbol_map': {}})
    if isinstance(str_word, dict):
      self.unit_info = str_word
      self.str_word = str_word['word']
      self.unit_info['word'] = self.str_word
    for index in range(len(self.str_word)):
      self.dict_unit[index] = {}
      self.dict_unit[index]['symbol'] = self.str_word[index]
      self.dict_unit[index]['type'] = ''
    self.keys = self.dict_unit.keys()

  def hasSymbol(self, symbol):
    return symbol in self.str_word

class Sentence(_Unit):
  """ Класс объекта предложения. Индексы списка и ключи словаря должны совпадать.
      При инициализации класса ему передаётся предложение в виде списка слов."""
  old_index = None
  new_index = None

  def _update_added_unit(self, subunit):
    _subunit = {
    'feature': [],
    'link': [],
    'homogeneous_link': [], # ссылки на однородные члены
    'type': 'real', # действительное слов. Есть ещё мнимое - такое слово, которое добавляется для удобства анализа.
    'base': '',
    'case': '',
    'notword': '',
    'start_pmark': [], 'end_pmark': [], 'around_pmark': []
    }
    subunit.update(_subunit)

  def __init__(self, words):
    self._init(properties_with_indexes=['link', 'homogeneous_link'], unit_info={'end':''})

    if isinstance(words, dict):
      for index, word in words.items():
        if isinstance(word, dict): word = Word(word)
        if isinstance(index, (unicode, str)): index = int(index)
        self.dict_unit[index] = word
      #self.position = 0
    else:
      for index, word in enumerate(words):
        self._update_added_unit(word)
        self.dict_unit[index] = word
    self.keys = self.dict_unit.keys()

  def getByCharacteristic(self, name, value):
    """ Извлекает слова, соответствующие характеристике.
        Возвращает словарь Индекс:Слово """
    results = {}
    for index, word in self.dict_unit.items():
      if name in word:
        # проверяем наличие индекса в списке ссылок
        if name in ['link', 'homogeneous_link'] and value in word[name]:
          results[index] = word
        # иначе просто сравниваем
        elif name in word and word[name] == value:
          results[index] = word
    return results

  def getByCharacteristicFeatures(self, name, value):
    """ То же, только ищет во featue'ах.
        Возвращает словарь Индекс:СписокFeature'в"""
    results = {}
    items = self.dict_unit.items()
    for index, word in items:
      features = word['feature']
      results[index] = []
      for feature in features:
        if name in feature and feature[name] == value:
          results[index].append(feature)
      if len(results[index]) == 0: del results[index]
    return results

  def addFeature(self, index, *indexes):
    """ Добавляет к слову определения и обстоятельства как его характеристику
        Первый аргумент - индекс главного слова, следующие аргументы -
        индексы обстоятельств и определений.
        Порядок значений второго аргумента может быть произвольным. """
    indexes = set(indexes)
    word = self.dict_unit[index]
    # добавляем определения или обстоятельства
    for _index in indexes:
      feature = self.dict_unit[_index]
      feature['index'] = _index
      word['feature'].append(feature)
    # удаляем из предложения
    self.delByIndex(*indexes)

  def getFeature(self, index):
    return self.dict_unit[index]['feature']

  def addLink(self, index_parent, index_obient): # parent = control
    """ Устанавливает ссылку """
    if index_obient not in self.dict_unit[index_parent]["link"]:
      self.dict_unit[index_parent]["link"].append(index_obient)

  def getObient(self, index):
    """ Возвращает индексы тех слов, которые подчиняются слову по
        переданому индексу"""
    return self.dict_unit[index]["link"]

  def getControl(self, index):
    """ Возвращает индексы тех слов, которым подчинено слово по
        переданому индексу. Всегда только один родитель. Если больше,
        то что-то не так с предложением."""
    indexes = []
    for _index, dword in self.dict_unit.items():
      # второе лог. выражение - слово не может подчиняться само себе.
      if index in dword['link'] and index != _index: indexes.append(_index)
    return indexes

  # к удалению
  def getSurroundingNeighbours(self, index):
    """ Возвращает двух соседей, то есть просто два окружающих слова,
        но не братьев. """
    left = right = None
    if index != 0: left = self.dict_unit[index-1]
    if index != len(self.dict_unit)-1: right = self.dict_unit[index+1]
    return left, right

  def addHomogeneous(self, *steps):
    """ Устанавливает однородность членам """
    indexes = [self.keys[self.position+step] for step in steps]#list(indexes)
    another_indexes = []
    for index in indexes:
      another_indexes.extend(self.dict_unit[index]['homogeneous_link'])
    indexes.extend(another_indexes)
    indexes = list(set(indexes))
    for _index in indexes:
      for index in indexes:
        if index != _index and _index not in self.dict_unit[index]['homogeneous_link']:
          self.dict_unit[index]['homogeneous_link'].append(_index)

  def getHomogeneous(self, index, inclusive=False): # inclusive - включительно с поданным индексом
    """ Возвращает слова, однородные переданному """
    homogeneous = self.dict_unit[index]['homogeneous_link']
    if inclusive: homogeneous.append(index)
    return homogeneous

  def getIndexesOfFirstWords(self):
    ''' Возвращает индексы первых слов. Первыми являютсмя те слова в предложении,
        на которые никто не ссылается. Возврашщает список индексов однородных слов.'''
    indexes = []
    for index, word in self.dict_unit.items():
      if not self.getControl(index): indexes.append(index)
    return indexes

class Text(_Unit):
  """ Класс объекта ткста.
      Возможности: анализ, обработка (изменение времени и прочее)
  """
  def __init__(self, sentences):
    self._init()
    for index, sentence in enumerate(sentences):
      self.dict_unit[index] = sentence
