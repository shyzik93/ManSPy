from manspy.utils.unit.base_unit import BaseUnit, errorManager


class Sentence(BaseUnit):
    """ Класс объекта предложения. Индексы списка и ключи словаря должны совпадать.
        При инициализации класса ему передаётся предложение в виде списка слов."""
    old_index = None
    new_index = None

    def __init__(self, words, imports=None):
        BaseUnit.__init__(self, words, unit_info={'end': ''}, parent={'name': 'sentence', 'value': self}, imports=imports)
        self.error = errorManager('graphmath', 'morph', 'postmorph', 'synt')

    def getByCharacteristic(self, name, value):
        """ Извлекает слова, соответствующие характеристике.
            Возвращает словарь Индекс:Слово """
        results = {}
        for index, word in self.subunit_info.items():
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
        items = self.subunit_info.items()
        for index, word in items:
            features = word['feature']
            results[index] = []
            for feature in features:
                if name in feature and feature[name] == value:
                    results[index].append(feature)
            if len(results[index]) == 0:
                del results[index]
        return results

    def addFeature(self, index, *indexes):
        """ Добавляет к слову определения и обстоятельства как его характеристику
            Первый аргумент - индекс главного слова, следующие аргументы -
            индексы обстоятельств и определений.
            Порядок значений второго аргумента может быть произвольным. """
        indexes = set(indexes)
        word = self.subunit_info[index]
        # добавляем определения или обстоятельства
        for _index in indexes:
            feature = self.subunit_info[_index]
            feature['is_feature_for'] = index # все слова в списке должны иметь свойство "is_свойство_for" равному индексу главного слова.
            word['feature'].append(feature)
        # удаляем из предложения
        self.delByIndex(*indexes)

    def getFeature(self, index):
        return self.subunit_info[index]['feature']

    def addLink(self, word_parent, word_obient): # parent = control
        """ Устанавливает ссылку """
        if word_obient.index not in self.subunit_info[word_parent.index]["link"]:
            self.subunit_info[word_parent.index]["link"].append(word_obient.index)

    def getObient(self, index):
        """ Возвращает индексы тех слов, которые подчиняются слову по
            переданому индексу"""
        return self.subunit_info[index]['link']

    def getControl(self, index):
        """ Возвращает индексы тех слов, которым подчинено слово по
            переданому индексу. Всегда только один родитель. Если больше,
            то что-то не так с предложением."""
        indexes = []
        for _index, dword in self.subunit_info.items():
            # второе лог. выражение - слово не может подчиняться само себе.
            if index in dword['link'] and index != _index: indexes.append(_index)
        return indexes

    # к удалению
    def getSurroundingNeighbours(self, index):
        """ Возвращает двух соседей, то есть просто два окружающих слова,
            но не братьев. """
        left = right = None
        if index != 0:
            left = self.subunit_info[index-1]
        if index != len(self.subunit_info)-1:
            right = self.subunit_info[index+1]
        return left, right

    def addHomogeneous(self, *steps):
        """ Устанавливает однородность членам """
        indexes = [self.keys[self.position+step] for step in steps]#list(indexes)
        another_indexes = []
        for index in indexes:
            another_indexes.extend(self.subunit_info[index]['homogeneous_link'])
        indexes.extend(another_indexes)
        indexes = list(set(indexes))
        for _index in indexes:
            for index in indexes:
                if index != _index and _index not in self.subunit_info[index]['homogeneous_link']:
                  self.subunit_info[index]['homogeneous_link'].append(_index)

    def getHomogeneous(self, index, inclusive=False): # inclusive - включительно с поданным индексом
        """ Возвращает слова, однородные переданному """
        homogeneous = self.subunit_info[index]['homogeneous_link']
        if inclusive: homogeneous.append(index)
        return homogeneous

    def getIndexesOfFirstWords(self):
        ''' Возвращает индексы первых слов. Первыми являютсмя те слова в предложении,
            на которые никто не ссылается. Возврашщает список индексов однородных слов.'''
        indexes = []
        for index, word in self.subunit_info.items():
            if not self.getControl(index):
                indexes.append(index)

        return indexes

    def addCombineWord(self, type_combine_word, *indexes):
        word = self.subunit_info[indexes.pop()]
        word['combine_type'] = type_combine_word

    def getCombineWord(self, type_combine_word, index):
        return self.subunit_info[index]['combine_words']
