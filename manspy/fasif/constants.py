NAME_LANG = r'[A-Z][a-z]+'
WORD = r'[a-zа-яёĉĝĥĵŝŭ]+'
WORD_WITH_PREPOSITION = '(?:'+WORD+')?[ \t]*'+WORD

NAME_PYTHON_OBJ = r'[_a-zA-Z][_0-9a-zA-Z]*'
NAME_INTERNAL_OBJ = r'\$'+NAME_PYTHON_OBJ
PATH_FUNCTION = r'(?:'+NAME_PYTHON_OBJ+'/)+'+NAME_PYTHON_OBJ
ALL_NAMES_FUNCTION = r'(?:'+PATH_FUNCTION+'|'+NAME_INTERNAL_OBJ+')'

# Парсинг Verbs
STRING_VERBS_TITLE = r'^'+ALL_NAMES_FUNCTION+'$'
#STRING_VERBS_BODY = r'^ {4}'+NAME_LANG+'[ \t]*:[ \t]*'+WORD_WITH_PREPOSITION+'[ \t]*$'
STRING_VERBS_BODY = r'^ {4}('+NAME_LANG+')[ \t]*:[ \t]*('+WORD_WITH_PREPOSITION+'(?:[ \t]*,[ \t]*'+WORD_WITH_PREPOSITION+')*)[ \t]*$'

STRING_VERBS_TITLE2 = r'^('+ALL_NAMES_FUNCTION+')$'
#STRING_VERBS_BODY2 = r'^ {4}('+NAME_LANG+')[ \t]*:[ \t]*('+WORD_WITH_PREPOSITION+')[ \t]*$'

# Парсинг WordCombination

STRING_DESTINATION_TITLE = r'^[_a-zA-Z0-9]+[ \t]*:[ \t]*'+PATH_FUNCTION+'[ \t]*$'
STRING_DESTINATION_BODY = r'^ {4}'+NAME_LANG+'[ \t]*:[ \t]*'+WORD+'[ \t]*$'
STRING_ARGUMENT_TITLE1 = r'^'+NAME_PYTHON_OBJ+'[ \t]+[yn][l]?[ \t]*(;[ \t]*'+NAME_LANG+'[ \t]*)+$'
STRING_ARGUMENT_BODY = r'^ {4}[-_+a-zA-Z0-9а-яА-ЯёЁ]+[ \t]*(;[ \t]*('+WORD+')?[ \t]*)+$'
STRING_ARGUMENT_TITLE2 = r'^'+NAME_PYTHON_OBJ+'[ \t]+[yn][l]?[ \t]*$'
STRING_WCOMB_TITLE = r'^'+NAME_LANG+'$'
#STRING_WCOMB_ARGWORD = r'^ {4}'+WORD_WITH_PREPOSITION+'[ \t]*:[ \t]*'+WORD+'[ \t]*(,[ \t]*'+WORD+'[ \t]*)*$' # первое слово - предлог (иногда нужен)
STRING_WCOMB_ARGWORD = r'^ {4}('+WORD_WITH_PREPOSITION+'[ \t]*:[ \t]*'+WORD+'[ \t]*(,[ \t]*'+WORD+'[ \t]*)*;*)+$' # первое слово - предлог (иногда нужен)
STRING_WCOMB = r'^ {4}('+WORD+')?([ \t]+'+WORD+')*[ \t]*$'  # Не должо совпадать с названием языка!

not_to_db = ['nombr', 'cifer']