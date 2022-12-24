from manspy.utils.unit.base_unit import BaseUnit


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
            symbols.append({'type': '', 'symbol': symbol})

        unit_info = {
            'word': self.str_word,
            'symbol_map': {},
            'feature': [],
            'link': [],
            'homogeneous_link': [],  # ссылки на однородные члены
            'type': 'real',
            # действительное слов. Есть ещё мнимое - такое слово, которое добавляется для удобства анализа.
            'start_pmark': [], 'end_pmark': [], 'around_pmark': [],
            'combine_words': []
        }
        parent = {'name': 'word', 'value': self}
        BaseUnit.__init__(self, symbols, unit_info, parent)

    def hasSymbol(self, symbol):
        return symbol in self.str_word

    def getUnit(self, _type, info0='members', info1='members', info2='info'):
        if _type == 'str':
            symbols = [sunit['symbol'] for sunit in self.subunit_info.values()]
            return ''.join(symbols)

        return super().getUnit(_type, info0, info1, info2)
