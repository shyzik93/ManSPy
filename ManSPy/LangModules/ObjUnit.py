# -*- coding: utf-8 -*-
# Author: Ra93POL
# Date: 2.12.2014 - nowdays
import copy

class _Unit():
  ''' unit(index) - извлечение подюнита
      unit(index, name) - извлечение характеристики подюнита
      unit(index, name, value) - изменение характеристики подюнита
      unit[name] - извлечение характеристики юнита
      unit[name] = value - изменение характеристики юнита
      name in unit - проверка наличия ключа характеристики юнита
      len(unit) - извлечение длины юнита

      Юнита - это предложение или слово. Подюнит - их составляющие:
      для предложения - это слова, для слов - это символы'''
  # Работа с информацией о юните в целом
  def __setitem__(self, key, value): self.unit_info[key] = value
  def __getitem__(self, key): return self.unit_info[key]
  def __contains__(self, name): return name in self.unit_info

  #def __repr__(self): return self.__class__.__name__ + "(" + str(self.full_info) + ")"
  def __repr__(self): return self.__class__.__name__ + "(" + str(self.unit_info) + ")"
  def items(self): return self.unit_info.items()
  def update(self, _dict): self.unit_info.update(_dict)

  # Работа с информацией о составляющих юнит (подюнитов)
  def __len__(self): return len(self.dict_unit)
  def __call__(self, index, name=None, value=None):
    if name == None: return self.dict_unit[index]
    elif value == None: return self.dict_unit[index][name]
    self.dict_unit[index][name] = value

  # Прочее
  def getLen(self, func=None):
    """ Возвращает длину юнита (кол-во подюнитов). Может применить к длине функцию,
        например range, после этого возвратится список """
    if func == None: return len(self.dict_unit)
    else: return func(len(self.dict_unit))

  def _go_depth(self, el, info1, info2):
    if isinstance(el, Sentence): return el.getSentence('dict', info1)
    elif isinstance(el, Word): return el.getWord('dict', info2)
    elif isinstance(el, dict):
      _el = {}
      for k, v in el.items(): _el[k] = self._go_depth(v, info1, info2)
      return _el
    elif isinstance(el, list):
      _el = []
      for v in el: _el.append(self._go_depth(v, info1, info2))
      return _el
    else: return el

  def getUnit(self, Type, info1='members', info2='info'):
    if Type == 'dict':
      if info2 == 'info': dct = self.unit_info
      elif info2 == 'members': dct = self.dict_unit
      elif info2 == 'all': dct = self.full_info
      dct = copy.deepcopy(dct)
      return self._go_depth(dct, info1, info2)
    elif Type == 'listSubUnits': # возвращает список подюнитв
      l = len(self.dict_unit)
      listDict = []
      for index in range(l): listDict.append(self.dict_unit[index])
      return listDict

class Word(_Unit):
  """ Класс объекта слова.
      При инициализации класса ему передаётся слово в виде строки. """  
  def __init__(self, str_word):
    self.unit_info = {}    # не перемещать!
    self.dict_unit = {}    # не перемещать!
    self.full_info = {'unit_info': self.unit_info, 'unit': self.dict_unit}    # не перемещать!
    self.str_word = str_word
    for index in range(len(str_word)):
      self.dict_unit[index] = {}
      self.dict_unit[index]['symbol'] = self.str_word[index]
      self.dict_unit[index]['type'] = ''
    self.unit_info = {'word': self.str_word, 'symbol_map': {}}

  def hasSymbol(self, symbol):
    return symbol in self.str_word

""" Функции для работы со стандартными структурами данных """

def dictOrder(d, old_index=None):
  """ Синхронизирует числовые ключи словаря, то есть смещает их.
      Возвращает список индексов, которые отсутствовали во входном словаре.
      Значения словаря сохраняют прежний порядок.
      Аргумент old_index - передаётся, если нужно узнать новый индекс
      вместо старого."""
  deleted = [] # индексы некогда удалённых слов, в порядке возрастания
  prev_sdvig = 0

  #print d
  prev_index = -1
  sdvig = 0
  for index, dict_unit in d.items():
    sdvig = index - prev_index - 1
    if sdvig > prev_sdvig:
      # добавляем все удалённые индексы
      _sdvig = sdvig-prev_sdvig
      while _sdvig > 0:
        deleted.append(index-_sdvig)
        _sdvig -= 1
    if sdvig > 0:
      d[index-sdvig] = d[index]
      del d[index]
    #print "sdvig: ", sdvig
    if old_index == index: old_index = index-sdvig
    prev_index = index-sdvig
    prev_sdvig = sdvig
  #print deleted
  #print d
  return deleted, old_index

class Sentence(_Unit):
  """ Класс объекта предложения. Индексы списка и ключи словаря должны совпадать.
      При инициализации класса ему передаётся предложение в виде списка слов."""
  old_index = None
  new_index = None

  def __init__(self, words):
    self.unit_info = {}    # не перемещать!
    self.dict_unit = {}    # не перемещать!
    self.full_info = {'unit_info': self.unit_info, 'unit': self.dict_unit}    # не перемещать!
    for index in range(len(words)):
      word = words[index]
      word['feature'] = []
      word['link'] = []
      word['homogeneous_link'] = [] # ссылки на однородные члены
      word['type'] = 'real' # действительное слов. Есть ещё мнимое - такое слово, которое добавляется для удобства анализа.
      self.dict_unit[index] = word

  def _syncLinks(self, words, deleted, parametr_name):
    """ Синхронизирует ссылки в словах """
    for word in words:
      for indexLink in word[parametr_name]:
        t = 1
        index = word[parametr_name].index(indexLink)
        for indexDel in deleted:
          if indexLink > indexDel:
            word[parametr_name][index] -= t
          elif indexLink == indexDel:
            del word[parametr_name][index]
          t =+ 1

  def _sync(self):
    """ Синхронизирует ключи словаря, то есть смещает их.
        Используется после удаления слов. """
    deleted, self.old_index = dictOrder(self.dict_unit, self.old_index)
    # синхронизируем ссылки
    self._syncLinks(self.dict_unit.values(), deleted, 'link')
    self._syncLinks(self.dict_unit.values(), deleted, 'homogeneous_link')

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

  def delByCharacteristic(self, name, value):
    """ Удаляет слова, содержащие определённые характеристики """
    for index, word in self.dict_unit.items():
      if name in word:
        if word[name] == value:
          del self.dict_unit[index]
    self._sync()

  def delByIndex(self, *indexes):
    """ Удаляет слово по его индексму или самому слову """
    for index in indexes:
      del self.dict_unit[index]
    self._sync()
    
  def delByIndexWithoutSync(self, *indexes):
    """ После удаления не синхронизирует ссылки и индексы. """
    for index in indexes:
      del self.dict_unit[index]

  def GetAndDel(self, index):
    word = self.dict_unit[index]
    self._syncLinks([word], [index])
    self.delByIndex(index)
    return word    

  def addFeature(self, index, *indexes):
    """ Добавляет к слову определения и обстоятельства как его характеристику
        Первый аргумент - индекс главного слова, следующие аргументы -
        индексы обстоятельств и определений.
        Порядок значений второго аргумента может быть произвольным. """
    indexes = list(indexes)
    # удаляем повторяющиеся индексы
    i = 0
    while i < len(indexes):
      if indexes.count(indexes[i]) > 1: del indexes[i]
      else: i += 1
    word = self.dict_unit[index]
    # добавляем определения или обстоятельства
    for index_feature in indexes:
      feature = self.dict_unit[index_feature]
      word['feature'].append(feature)
    # удаляем из предложения
    self.old_index = index
    self.delByIndex(*indexes)
    return self.old_index

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

  def getEqWord(self, word):
    """ Возвращае словарь идентичных слов """
    pass

  def functionToValues(self, index, parametr_name, function):
    """ Метод применяет функцию к каждому элементу характеристики слова.
        То есть, можеть менять элементы характеристик feature, link. """
    word = self.dict_unit[index]
    for i in range(len(word[parametr_name])):
      word[parametr_name][i] = function(word[parametr_name][i])

  def getSurroundingNeighbours(self, index):
    """ Возвращает двух соседей, то есть просто два окружающих слова,
        но не братьев. """
    if index != 0: left = self.dict_unit[index-1]
    else: left = None
    if index != len(self.dict_unit)-1: right = self.dict_unit[index+1]
    else: right = None
    return left, right

  def addHomogeneous(self, *indexes):
    """ Устанавливает однородность членам """
    indexes = list(indexes)
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

  def forAllWords(self, index, func, *args):
    """ Применяет функцию к каждому слову.
        Передаваемая фукция должна возврать текущий индекс слова.
        Первым и вторым аргументами передаются индекс и предложение соответсвенно!
    """
    while index < len(self.dict_unit):
      index = func(index, self, *args)
      index += 1

class Text():
  """ Класс объекта ткста.
      Возможности: анализ, обработка (изменение времени и прочее)
  """
  def __init__(self):
    pass

if __name__ == '__main__':
  s = "Hello0 my1 smarControl2 t3 home4 I5 createdObient6 your7 intellect8"
  s = Sentence(s.split())

  #s.GetSet(1, "bl", "gggg")
  #s.GetSet(2, "bl", "gggg")
  s.GetSet(7, "bl", "gggg")

  s.delByCharacteristic("bl", "gggg")
  print("111111111111111111")
  #s.delByWI(0)
  #s.delByWI("your7")

  s.addLink(2, 6)
  s.delByIndex(0)
  s.delByIndex(4)

  print s.getSentence("str"), '\n'
  print s.getSentence("list"), '\n'
  print s.getSentence("dict"), '\n'
  print s.getSentence("beautyDict"), '\n'
