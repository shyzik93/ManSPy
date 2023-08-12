import copy
import re


class errorManager:
    """ power_level - the dangerous' level of error
        if power_level = 0 - the error are not dangerous. It ignores.
        if power_level = 1 - the IL will not execute. """

    def __init__(self, *group_names):
        self.errors = {}
        power_levels = [0, 1]
        for group_name in group_names:
            errors = {}
            for power_level in power_levels: errors[power_level] = []
            self.errors[group_name] = errors

    def add(self, group_name, message, power_level):
        print(group_name, message, power_level)
        self.errors[group_name][power_level].append(message)

    def get(self, group_name, power_level):
        return self.errors[group_name][power_level]

    def getLen(self, group_name, *power_levels):
        l = 0
        for power_level in power_levels:
            l += len(self.errors[group_name][power_level])
        return l

    # def getNamesError(self): return self.errors.keys()
    def getRaw(self):
        return self.errors

    def beautyPrint(self):
        pass


class BaseUnit:
    """
    `unit[index]` - извлечение подъюнита
    `unit[index][name]` - извлечение характеристики подъюнита
    `unit[index][name]` = value - изменение характеристики подъюнита

    `unit[name]` - извлечение характеристики юнита
    `unit[name] = value` - изменение характеристики юнита
    `del unit[name]` - удалить характеристику юнита
    `unit[name] = None` - удалить характеристику юнита
    `name in unit` - проверка наличия ключа характеристики юнита
    `len(unit)` - извлечение длины юнита (количество подъюнитогв)

    Если значение характеристика равно None, то такая характеристика считается несуществующей.

    Юнит - это предложение или слово. Подъюнит - их составляющие:
    для предложения - это слова, для слов - это символы
    """

    def __init__(self, subunits=None, unit_info=None, parent=None, imports=None):
        self.unit_info = {'max_index': -1, 'index': None}
        self.subunit_info = {}
        self.full_info = {'unit_info': self.unit_info, 'unit': self.subunit_info}

        self.position = 0
        self.keys = []

        self.subunits_copy = {}

        if unit_info:
            self.unit_info.update(unit_info)

        if subunits:
            self.load_subunits(subunits, parent)

        if imports:
            self.import_unit(imports)

        self.parent = parent

    def import_unit(self, data):
        from manspy.utils.unit import Word, Sentence, Text

        if 'feature' in data['unit_info']:
            for index, subunit in enumerate(data['unit_info']['feature']):
                _subunit = locals()[subunit['unit_type']]({})
                _subunit.import_unit(subunit)
                data['unit_info']['feature'][index] = _subunit

        for index, subunit in data['unit'].items():
            if 'unit_type' not in subunit or subunit['unit_type'] == 'dict':
                _subunit = subunit
            else:
                _subunit = locals()[subunit['unit_type']]({})
                _subunit.import_unit(subunit)

            data['unit'][index] = _subunit

        self.full_info = copy.deepcopy(data)
        self.unit_info = self.full_info['unit_info']
        self.subunit_info = {int(index): unit for index, unit in self.full_info['unit'].items()}
        self.keys = list(self.subunit_info.keys())

    def export_unit(self, ignore_units=None):
        data = copy.deepcopy(self.full_info)

        data['unit_type'] = self.__class__.__name__

        if 'feature' in data['unit_info']:
            for index, subunit in enumerate(data['unit_info']['feature']):
                data['unit_info']['feature'][index] = subunit.export_unit(ignore_units)

        if ignore_units and data['unit'] and isinstance(list(data['unit'].values())[0], ignore_units):
            data['unit'].clear()

        for index, subunit in data['unit'].items():
            if isinstance(subunit, dict):
                break

            data['unit'][index] = subunit.export_unit(ignore_units)

        return data

    def load_subunits(self, subunits, parent=None):
        """
        Загружает подъюниты из списка либо словаря.
        Словарь обычно используется при добавлении подъюнитов экспортированного юнита
        """
        self.unit_info['max_index'] = len(subunits) - 1

        """if isinstance(subunits, list): iterator = enumerate(subunits)
        elif isinstance(subunits, dict): iterator = subunits.items() # нерекомендаовано

        for index, subunit in iterator:
            if isinstance(index, str) and index.isdecimal():
                index = int(index)  # только для словаря
            if isinstance(subunit, dict) and isinstance(index, int):
                subunit['index'] = index
            self.subunit_info[index] = subunit"""

        if isinstance(subunits, list):

            for index, subunit in enumerate(subunits):
                subunit['index'] = index
                self.subunit_info[index] = subunit
                if parent and subunit['unit_type'] in ('Word', 'Sentence', 'Text'):
                    setattr(subunit, parent['name'], parent['value'])

        elif isinstance(subunits, dict):

            for index, subunit in subunits.items():
                index = index if isinstance(index, int) else int(index)
                subunit['index'] = index
                self.subunit_info[index] = subunit

        self.keys = list(self.subunit_info.keys())
        self.subunits_copy = self.subunit_info.copy()  # делаем неглубокую копию исходного предложения.

    # Работа с информацией о юните в целом

    def __setitem__(self, key, value):
        if key in self.unit_info and value is None:
            del self.unit_info[key]
            return

        self.unit_info[key] = value

    def __getitem__(self, key):
        """
        Извлекает значение свойства юнита либо подъюнит
        :param key: имя свойства либо индекс подъюнита
        :return: значение свойства юнита, если key - строка; подъюнит, если key - целое число.
        """
        if isinstance(key, str):
            return self.unit_info.get(key)
        elif isinstance(key, int):  # типа getByIndex()
            return self.subunit_info[key]
        else:
            raise Exception('unknown type of item key')

    def __delitem__(self, key):
        """
        Извлекает значение свойства юнита либо подъюнит
        :param key: имя свойства либо индекс подъюнита
        :return: значение свойства юнита, если key - строка; подъюнит, если key - целое число.
        """
        if isinstance(key, str):
            del self.unit_info[key]
        elif isinstance(key, int):
            del self.subunit_info[key]
        else:
            raise Exception('unknown type of item key')

    def __contains__(self, name):
        return self.unit_info.get(name) is not None

    # def __repr__(self): return self.__class__.__name__ + "(" + str(self.full_info) + ")"
    def __repr__(self):
        return self.__class__.__name__ + "(" + str(self.unit_info) + ")"

    def items(self):
        return self.subunit_info.items()  # аналогично itemsUnit() без индекса. Не рекомендуется. Только для внутреннего использования.

    def itemsInfo(self):
        return self.unit_info.items()

    def itemsUnit(self, index=None):
        return self.subunit_info.items() if index is None else self.subunit_info[index].items()

    def update(self, _dict):
        self.unit_info.update(_dict)

    # Работа с информацией о составляющих юнит (подюнитов)
    def __len__(self):
        """Возвращает длину юнита"""
        return len(self.subunit_info)

    @property
    def index(self):
        return self.unit_info['index']

    # Итератор
    def __iter__(self,
                 position=0):  # # аналогично itemsUnit() без индекса, но с возможностью управления текущей позицией. Для цикла for.
        self.position = position
        self.keys = list(self.subunit_info.keys())
        while self.position < len(self.keys) and self.position >= 0:
            index = self.keys[self.position]
            yield self.subunit_info[index]
            self.position += 1
        self.position = 0

    def iterFromByStep(self, step=0):
        position = self.position + step if step != None else 0
        return self.__iter__(position)

    def iterFromByIndex(self, index):
        position = list(self.keys).index(index)
        return self.__iter__(position)

    def jumpByStep(self, step=1):
        self.position += step  # аналог next()

    def jumpByIndex(self, index):
        self.position = self.keys.index(index)

    def delByStep(self, count=1, step=0, jump_step=-1):
        for c in range(count):
            del self.subunit_info[self.keys[self.position + step]]
        self.keys = list(self.subunit_info.keys())
        self.position += jump_step

    def delByPos(self, position):
        del self.subunit_info[self.keys[position]]
        self.keys = list(self.subunit_info.keys())

    def delByIndex(self, *indexes):
        for index in indexes:
            del self.subunit_info[index]
        self.keys = list(self.subunit_info.keys())

    def getByStep(self, step=0):
        return self.subunit_info[self.keys[self.position + step]]

    def getByPos(self, position):
        return self.subunit_info[self.keys[position]]

    def currentIndex(self, step=0):
        return self.keys[self.position + step]  # TODO: delete this method

    # Текущая позиция
    def isOutLeft(self, step=0):
        return self.position + step < 0

    def isFirst(self, step=0):
        return self.position + step == 0

    def isBetween(self, step=0):
        return self.position + step < len(self.subunit_info) - 1 and self.position + step > 0

    def isLast(self, step=0):
        return self.position + step == len(self.subunit_info) - 1

    def isOutRight(self, step=0):
        return self.position + step > len(self.subunit_info) - 1

    def isEntry(self, step=0):
        return self.position + step >= 0 and self.position + step < len(self.subunit_info)

    def getNeighbours(self, step=0):
        left = self.subunit_info[self.keys[self.position + step - 1]] if self.position != 0 else None
        right = self.subunit_info[self.keys[self.position + step + 1]] if self.position != len(self.keys) - 1 else None
        return left, right

    # Прочее

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
        setdict = {'list': {'setvalue': 'in', 'negative': False, 'names': []},
                   'subiv': {'setvalue': 'ignore', 'negative': False, 'names': []}, }
        setstring = re.split(r' *; *', setstring.lower())
        for _setstring in setstring:
            # print setstring, re.findall(r'([a-z]+) *: *([a-z]+) *(?:- *(\^[a-z]+(?: *, *[a-z]+)?))?', _setstring)
            if not _setstring: continue
            setname, setvalue, names = \
            re.findall(r'([a-z]+) *: *([a-z]+) *(?:- *(\^[a-z]+(?: *, *[a-z]+)?))?', _setstring)[0]
            negative = False if not names or names[0] != '^' else True
            names = names[1:] if negative else names
            names = re.split(r' *, *', names)
            names = [] if not names[0] else names
            setdict[setname] = {'setvalue': setvalue, 'negative': negative, 'names': names}

        return setdict

    # Коллекция функций для массовой работы с подъюнитами, имеющих одинаковые значения свойств.
    def _compare_subunit(self, subunit, properties, setdict):
        counter = len(properties)
        for name, value in properties.items():
            if not isinstance(value, tuple):
                value = (value,)

            if isinstance(value[0], (list, tuple, dict)) and setdict['setvalue'] == 'in':
                if name not in subunit:
                    continue

                _counter = len(value)
                for _value in value:
                    if _value in subunit[name]:
                        _counter -= 1

                if not _counter:
                    counter -= 1
            else:
                if subunit[name] in value:
                    counter -= 1

        if not counter:
            return True

    def _compare_subunits_in_values(self, subunit, properties, setdict):
        _subunits = []
        for name, value in subunit.itemsInfo():
            if not isinstance(value, list): continue
            for _subunit in value:
                if not isinstance(_subunit, type(subunit)): continue
                if self._compare_subunit(_subunit, properties, setdict): _subunits.append(_subunit)

        return _subunits

    def getByValues(self, setstring='', **properties):
        ''' Возвращает слова, имеющие одниаковые значения свойств properties '''
        setdict = self._parseSettingsString(setstring)
        for index, subunit in self.subunit_info.items():
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
            for _subunit in _subunits: _subunit.update(new_properties)
            if subunit: subunit.update(new_properties)

    def _getByProperty(self, result, eq, not_eq, everywhere, list_names, units):
        ''' units - список из словарей символов или объектов Слово, Предложение, Текст '''
        for unit in units:
            is_true = True
            for name, values in eq.items():
                if name in unit and str(unit[name]) in values: continue
                is_true = False
                break
            # if not is_true: continue

            for name, values in not_eq.items():
                if name not in unit or str(unit[name]) not in values: continue
                is_true = False
                break
            # if not is_true: continue

            if is_true: result.append(unit)

            # поиск в значении свойств, если значение - список.
            if unit is BaseUnit:
                names = unit.itemsInfo()
            else:
                names = unit.items()

            for name, value in names:
                if not isinstance(value, (list,)):
                    continue

                if len(value) == 0 or not (value[0] is BaseUnit or not isinstance(value[0], dict)):
                    continue  # пропускаем лишние рекурсивные вызовы

                if everywhere and name not in list_names:
                    self._getByProperty(result, eq, not_eq, everywhere, list_names, value)
                elif not everywhere and name in list_names:
                    self._getByProperty(result, eq, not_eq, everywhere, list_names, value)

    def getByProperty(self, find_in, **properties):
        ''' Возвращает список подъюнитов'''
        eq = {}
        not_eq = {}

        everywhere = False  # ищем только в указанных свойствах
        result = []

        for name, values in properties.items():
            if not isinstance(values, list): values = [values]
            for value in values:
                if len(value) > 0 and value[0] == '^':
                    if name not in not_eq: not_eq[name] = []
                    not_eq[name].append(value[1:])
                else:
                    if name not in eq: eq[name] = []
                    eq[name].append(value)

        if len(find_in) > 0 and find_in[0] == '^':
            everywhere = True  # ищем во всех свойствах, кроме указанных
            find_in = find_in[1:]
        list_names = find_in.split(',') if find_in else []

        self._getByProperty(result, eq, not_eq, everywhere, list_names, self.subunit_info.values())

        return result

    def remove(self):
        if self.parent:
            index = self.unit_info['index']
            del self.parent['value'].subunit_info[index]
