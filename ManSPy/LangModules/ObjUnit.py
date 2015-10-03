# -*- coding: utf-8 -*-
# Author: Ra93POL
# Date: 2.12.2014
""" Модуль, содержащий объекты предложения и текста. Не зависимы от ЕЯ.
    Объекты предоставляют удобный интерфейс,
    что позволяет разгрузить модули ЕЯ от руктинного и отвлекающего кода.
"""

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
  for index, dict_word in d.items():
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

class Sentence():
  """ Класс объекта предложения. Индексы списка и ключи словаря должны совпадать.
      При инициализации класса ему передаётся предложение в виде списка слов.
  """
  dict_sentence = {}
  old_index = None
  new_index = None

  def __init__(self, list_sentence):
    self.dict_sentence = {index: {} for index in range(len(list_sentence))}
    for index in range(len(list_sentence)):
      self.dict_sentence[index]['word'] = list_sentence[index]
      self.dict_sentence[index]['feature'] = []
      self.dict_sentence[index]['link'] = []
      self.dict_sentence[index]['homogeneous_link'] = [] # ссылки на однородные члены
      self.dict_sentence[index]['type'] = 'real' # действительное слов. Есть ещё мнимое - такое слово, которое добавляется для удобства анализа.

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
    deleted, self.old_index = dictOrder(self.dict_sentence, self.old_index)
    # синхронизируем ссылки
    self._syncLinks(self.dict_sentence.values(), deleted, 'link')
    self._syncLinks(self.dict_sentence.values(), deleted, 'homogeneous_link')

  def __getlen__(self): return len(self.dict_sentence)

  def __getitem__(self, index):
    if index in self.dict_sentence: return self.dict_sentence[index]
    else: return None

  def GetSet(self, index, parametr_name=None, parametr_value=None): # Get or Set Data
    """ Получение информации о слове по имени слова или по его порядковому номеру.
        Данные возвращаются все или только один параметр.
        Или же изменение данных, если указаны все три параметра."""
    if parametr_name == None:
      return self.dict_sentence[index]
    elif parametr_value == None:
      return self.dict_sentence[index][parametr_name]
    else:
      self.dict_sentence[index][parametr_name] = parametr_value
  
  def getByCharacteristic(self, name, value):
    """ Извлекает слова, соответствующие характеристике.
        Возвращает словарь Индекс:Слово """
    results = {}
    for index, word in self.dict_sentence.items():
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
    items = self.dict_sentence.items()
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
    for index, word in self.dict_sentence.items():
      if name in word:
        if word[name] == value:
          del self.dict_sentence[index]
    self._sync()

  def delByIndex(self, *indexes):
    """ Удаляет слово по его индексму или самому слову """
    for index in indexes:
      del self.dict_sentence[index]
    self._sync()
    
  def delByIndexWithoutSync(self, *indexes):
    """ После удаления не синхронизирует ссылки и индексы. """
    for index in indexes:
      del self.dict_sentence[index]

  def GetAndDel(self, index):
    word = self.dict_sentence[index]
    self._syncLinks([word], [index])
    self.delByIndex(index)
    return word
    #for indexLink in word["link"]:
    #  t = 0
    #  if indexLink < index:
    #    index2 = word["link"].index(indexLink)
    #    word["link"][index2] = indexLink - t
    #  elif indexLink == indexDel:
    #    index2 = word["link"].index(indexLink)
    #    del word["link"][index2]
    #  t =+ 1
    

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
    word = self.dict_sentence[index]
    # добавляем определения или обстоятельства
    for index_feature in indexes:
      feature = self.dict_sentence[index_feature]
      word['feature'].append(feature)
    # удаляем из предложения
    self.old_index = index
    self.delByIndex(*indexes)
    return self.old_index

  def getFeature(self, index):
    return self.dict_sentence[index]['feature']

  def addLink(self, index_parent, index_obient): # parent = control
    """ Устанавливает ссылку """
    if index_obient not in self.dict_sentence[index_parent]["link"]:
      self.dict_sentence[index_parent]["link"].append(index_obient)

  def getObient(self, index):
    """ Возвращает индексы тех слов, которые подчиняются слову по
        переданому индексу"""
    return self.dict_sentence[index]["link"]

  def getControl(self, index):
    """ Возвращает индексы тех слов, которым подчинено слово по
        переданому индексу. Всегда только один родитель. Если больше,
        то что-то не так с предложением."""
    indexes = []
    for _index, dword in self.dict_sentence.items():
      # второе лог. выражение - слово не может подчиняться само себе.
      if index in dword['link'] and index != _index: indexes.append(_index)
    return indexes

  def getEqWord(self, word):
    """ Возвращае словарь идентичных слов """
    pass

  def getSentence(self, Type):
    if Type == 'str':
      pass
    elif Type == 'dict': return self.dict_sentence
    elif Type == 'listDict':
      l = len(self.dict_sentence)
      listDict = []
      for index in range(l): listDict.append(self.dict_sentence[index])
      return listDict
    elif Type == 'forLogicDict':
      return "it must be ready for Logic module)))"
    elif Type == 'beautyDict':
      return "it must be beauty)))"

  def getLen(self, func=None):
    """ Возвращает длину предложения. Может применить к длине функцию,
        например range, после этого возвратится список """
    if func == None: return len(self.dict_sentence)
    else: return func(len(self.dict_sentence))

  def functionToValues(self, index, parametr_name, function):
    """ Метод применяет функцию к каждому элементу характеристики слова.
        То есть, можеть менять элементы характеристик feature, link. """
    word = self.dict_sentence[index]
    for i in range(len(word[parametr_name])):
      word[parametr_name][i] = function(word[parametr_name][i])

  def getSurroundingNeighbours(self, index):
    """ Возвращает двух соседей, то есть просто два окружающих слова,
        но не братьев. """
    if index != 0: left = self.GetSet(index-1)
    else: left = None
    if index != len(self.dict_sentence)-1: right = self.GetSet(index+1)
    else: right = None
    return left, right

  def addHomogeneous(self, *indexes):
    """ Устанавливает однородность членам """
    indexes = list(indexes)
    another_indexes = []
    for index in indexes:
      another_indexes.extend(self.dict_sentence[index]['homogeneous_link'])
    indexes.extend(another_indexes)
    indexes = list(set(indexes))
    for _index in indexes:
      for index in indexes:
        if index != _index and _index not in self.dict_sentence[index]['homogeneous_link']:
          self.dict_sentence[index]['homogeneous_link'].append(_index)

  def getHomogeneous(self, index, inclusive=False): # inclusive - включительно с поданным индексом
    """ Возвращает слова, однородные переданному """
    homogeneous = self.dict_sentence[index]['homogeneous_link']
    if inclusive: homogeneous.append(index)
    return homogeneous

  def forAllWords(self, index, func, *args):
    """ Применяет функцию к каждому слову.
        Передаваемая фукция должна возврать текущий индекс слова.
        Первым и вторым аргументами передаются индекс и предложение соответсвенно!
    """
    while index < len(self.dict_sentence):
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
