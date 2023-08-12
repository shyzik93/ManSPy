from manspy.analyzers.utils import get_func_common, get_func_wcomb
from manspy.storage.relation import Relation
from manspy.utils.constants import INDICATIVE, IMPERATIVE, MOOD, PRESENT, TENSE
from manspy.utils.unit import Sentence
from manspy.utils import importer


def Extraction2IL(relation, settings, subjects, predicate, arguments):
    verb = {'func_common': None, 'used_antonym': predicate['antonym'], 'answer_type': settings.answer_type}
    internal_sentence = {
        'type_sentence': 'fact',
        'verb': verb,
        'word_combinations': [],
        'subjects_word_combinations': []
    }
    if predicate[MOOD] == IMPERATIVE:
        internal_sentence['type_sentence'] = 'run'
    elif predicate[MOOD] == INDICATIVE and predicate[TENSE] == PRESENT:
        internal_sentence['type_sentence'] = 'fact'

    #  Вынимаем ФАСИФ глагола - сказуемого
    verb_id_group, str_func_common = get_func_common(relation, predicate['base'], settings)
    if str_func_common:
        verb['func_common'] = importer.import_action(str_func_common)

    # Вынимаем Фасиф словосочетаний - актантов
    for _argument in arguments:  # у подпредложения может быть несколько актантов
        str_import_get_value, str_import_set_value, finded_args, finded_set_by_antonym = get_func_wcomb(Sentence(_argument), settings, relation, verb_id_group)
        if finded_args is not None:
            word_combination = {
                'func_get_value': importer.import_action(str_import_get_value) if str_import_get_value else None,
                'func_set_value': importer.import_action(str_import_set_value) if str_import_set_value else None,
                'arguments': finded_args,
            }
            internal_sentence['word_combinations'].append(word_combination)
            if finded_set_by_antonym:
                verb['used_antonym'] = not verb['used_antonym']

    # Вынимаем Фасиф словосочетаний - субъектов
    for _subject in subjects:
        str_import_get_value, _, finded_args, __ = get_func_wcomb(Sentence(_subject), settings, relation, None)
        if finded_args is not None:
            word_combination = {
                'func_get_value': importer.import_action(str_import_get_value) if str_import_get_value else None,
                'func_set_value': None,
                'arguments': finded_args,
            }
            internal_sentence['subjects_word_combinations'].append(word_combination)

    return internal_sentence


def analyze(message):
    relation = Relation(message.settings)
    internal_sentences = {}
    # перебираем предложения
    il_index = 0
    for subjects_by_predicate, predicates, arguments_by_predicate in message.text:
        # перебираем однородные, придаточные и главные подпредложения
        for subjects, predicate, arguments in zip(subjects_by_predicate, predicates, arguments_by_predicate):
            internal_sentences[il_index] = Extraction2IL(relation, message.settings, subjects, predicate, arguments)
            il_index += 1

    return internal_sentences
