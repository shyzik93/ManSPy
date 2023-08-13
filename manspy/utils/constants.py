def generate_properties(str_properties_names):
    properties_names = str_properties_names.strip().split()
    for index_property, property_name in enumerate(properties_names):
        globals()[property_name] = index_property

    return len(properties_names)


# Названия свойств символа

TYPE = '1'

# SYMBOL_PROPERTIES_LENGTH = generate_properties("TYPE")

# Значения свойств символа: TYPE

LETTER = 1

# Названия свойств слова

MOSENTENCE = None
POSPEECH = None
NAME = None
CONJUNCTION_VALUE = None
DERIVATIVE = None  # значения свойства аналогичны POSPEECH
CATEGORY = None
NUMBER = None
ARTICLE_VALUE = None
CLASS = None
TENSE = None
MOOD = None
CASE = None

str_word_properties_names = """
MOSENTENCE POSPEECH NAME CONJUNCTION_VALUE DERIVATIVE CATEGORY NUMBER ARTICLE_VALUE CLASS TENSE MOOD CASE
"""
WORD_PROPERTIES_LENGTH = generate_properties(str_word_properties_names)

# Значения свойств слова: MOSENTENCE

DIRECT_SUPPLEMENT = 1
SUPPLEMENT = 2
PREDICATE = 3
SUBJECT = 4
DEFINITION = 5
CIRCUMSTANCE = 6

# Значения свойств слова: POSPEECH

ARTICLE = 1
ADVERB = 2
ADJECTIVE = 3
VERB = 4
NOUN = 5
PARTICLE = 6
PRONOUN = 7
PREPOSITION = 8
CONJUNCTION = 9
NUMERAL = 10

# Значения свойств слова: NAME

COMMON = 1
PROPER = 2

# Значения свойств слова: CONJUNCTION_VALUE

COORDINATING = 1
SUBORDINATING = 2

# Значения свойств слова: CASE

NOMINATIVE = 1
GENETIVE = 2
DATIVE = 3
INSTRUMENTAL = 4
ABLATIVE = 5
LOCATIVE = 6
UNDEFINED = 7
ACCUSATIVE = 8

# Значения свойств слова: CATEGORY

REFLEXIVE = 1
PERSONAL = 2
POSSESSIVE = 3

# Значения свойств слова: NUMBER

SINGULAR = 1
PLURAL = 2

# Значения свойств слова ARTICLE_VALUE

DEFINED = 1

# Значения свойств слова: CLASS

ORDINAL = 1
CARDINAL = 2

# Значения свойств слова: TENSE

PRESENT = 1
PAST = 2
FUTURE = 3

# Значения свойств слова: MOOD

INFINITIVE = 1
IMPERATIVE = 2
INDICATIVE = 3
SUBJUNCTIVE = 4

