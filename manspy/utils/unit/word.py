from manspy.utils.constants import TYPE
from manspy.utils.unit.base_unit import BaseUnit
from manspy.utils.unit.list_of_subunits import ListOfSubunits


class Word(BaseUnit):
    """
    Класс объекта слова.
    При инициализации класса ему передаётся слово в виде строки.

    Свойства юнита слова:
    - word - строковое представление слова
    - symbol_map -
    - feature - список определений слова
    - link - список на слова, зависимые от данного
    - homogeneous_link - список однородных членов
    - type
    - base - корень слова
    - case - падеж. Обычно только существительного,
    но также и для других частей речи, если, например, язык поддерживает согласование падежей для определений
    - notword
    - start_pmark
    - end_pmark
    - around_pmark
    - combine_words - список слов, являющихся составными для данного
    """
    def __init__(self, str_word):
        self.str_word = str_word
        self.sentence = None
        symbols = []
        for symbol in str_word:
            symbols.append({TYPE: '', 'symbol': symbol, 'unit_type': 'dict'})

        unit_info = {
            'word': self.str_word,
            'symbol_map': {},
            'feature': [],
            'link': [],
            'homogeneous_link': [],  # ссылки на однородные члены
            'type': 'real',
            # Действительное слово. Есть ещё мнимое - такое слово, которое добавляется для удобства анализа.
            'start_pmark': [], 'end_pmark': [], 'around_pmark': [],
            'combine_words': [],
        }
        BaseUnit.__init__(self, symbols, unit_info)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        if parent:
            self.links = ListOfSubunits(parent, self.unit_info['link'])
            self.homogeneous_links = ListOfSubunits(parent, self.unit_info['homogeneous_link'])

    @property
    def features(self):
        return self.unit_info['feature']

    def has_symbol(self, symbol):
        return symbol in self.str_word
