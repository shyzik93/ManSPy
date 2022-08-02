module: consrants.case
NOMINATIVE = 1  # именительный
ACCUSATIVE = 2  # винительный

module:constants.number
# Число
SINGULAR = 1  # единственное число
PLURAL = 2  # множественное число

# Имя
COMMON = 1  # имя нарицательное
PROP = 2  # имя собственное

# Части речи
NOUN = 1  # существительное
NUMERAL = 2 # числительное
ADVERB = 3  # наречие
PRONOUN = 4  # местоимение
ADJECTIVE = 5  # прилагательное
VERB = 6  # глагол
ARTICLE = 7  # артикль
PREPOSITION = 8  # предлог
CONJUCTION = 9  # союз

# Категории местоимений
POSSESSIVE = 1  # притяжательное

# Класс
ORDINAL = 1  # порядковое
CARDINAL = 2  # количественное

# Категория (группа) части речи
CONTENT = 1  # знаменательная
FUNCTION = 2  # служебная

# Функция союза
# COORDINATING = 1  #

# Члены предложения
DIRECT_SUPPLEMENT = 1  # Прямое дополнение
SUPPLEMENT = 2  # дополнение
SUBJECT = 3  # подлежащее
DEFINITION = 4  # определение
CIRCUMSTANCE = 5  # обстоятельство
PREDICATE = 6  # сказуемое

# В начале синтаксичесаого анализа из предложения должны быть удалены все служебные части речи.

# -----------------------------------

from dataclasses import dataclass


@dataclass
class Word:
    base: str  # корень слова
    source: str  # исходное слово, встреченное во входящем тексте
    antonym: bool  # употреблено как антоним корня (например, в есть соответсвующая приставка)
    # Свойства слова как части речи
    pospeech: int  # часть речи
    mospeech: int  #  член предложения
    derivative: int  # данная часть речи является производным от указанного
    # Свойства слова как члена предложения
    mospeech: int  #  член предложения


    #@dataclass
    #class WordNoun(Word):
    """ Имя существительное """
    group: int = CONTENT  # категория (группа) части речи
    case: int  # падеж
    number: int  # число
    name: int  # имя


    #@dataclass
    #class WordNumeral(Word):
    """ Имя числительное """
    group: int = CONTENT  # категория (группа) части речи
    number_value: int  # числовое значение
    class: int  # класс


   #@dataclass
   #class WordAdverb(Word):
    """ Наречие """
    group: int = CONTENT  # категория (группа) части речи


    #@dataclass
    #class WordPronoun(Word):
    """ Местоимение """
    group: int = CONTENT  # категория (группа) части речи
    category: int  # категория


    #@dataclass
    #class WordAdjective(Word):
    """ Имя прилагательное """
    group: int = CONTENT  # категория (группа) части речи
    case: int  # падеж
    number: int  # число


    #@dataclass
    #class WordVerb(Word):
    """ Глагол """
    group: int = CONTENT  # категория (группа) части речи


    #@dataclass
    #class WordArticle(Word):
    """ Артикль """
    group: int = FUNCTION  # категория (группа) части речи


    #@dataclass
    class WordPreposition(Word):
    """ Предлог """
    group: int = FUNCTION  # категория (группа) части речи


    #@dataclass
    #class WordConjuction(Word):
    """ Союз """
    group: int = FUNCTION  # категория (группа) части речи
    value: int  #  функция союза
