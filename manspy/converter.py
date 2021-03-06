import itertools

from manspy.unit import Sentence
from manspy.fasif import finder
from manspy.utils import importer

not_to_db = ['nombr', 'cifer']


def dproduct(dparentl):
    """
    Выполняет декартово (прямое) произведение над словарями в списке dparent1
    В стандартной библиотеке Python я этой функции не нашёл.
    Функция необходима для аргументных слов.
    :param dparentl: {'a': [1,2], 'b': [5,6]}
    :return: [{'a': 1, 'b':5}, {'a': 1, 'b':6}, {'a': 2, 'b':5}, {'a': 2, 'b':6}]
    """
    def _dproduct(resl, values, key):
        """
        [
            (('a',1), ('b',5)),
            (('a',1), ('b',6)),
            (('a',2), ('b',5)),
            (('a',2), ('b',6))
        ]
        """
        n = len(values)
        _resl = list(resl)
        for i, el in enumerate(resl, 0):
            for j in range(n - 1):
                _resl.insert(i * n, dict(el))
            for j in range(n):
                _resl[j + n * i][key] = values[j]
        return _resl
    prevchildl = [{}]
    for key, values in dparentl.items():
        prevchildl = _dproduct(prevchildl, values, key)
    return prevchildl


def dproduct2(dparent1):
    """ Второй вариант функции. TODO: Необходимо обе протестировать на скорость """
    l = [([k], v) for k, v in dparent1.items()]
    l = [[i for i in itertools.product(*subl)] for subl in l]
    l = [i for i in itertools.product(*l)]
    l = [dict(i) for i in l]
    return l


def is_in_hyperonym(hyperonyms, argvalue, R):
    for hyperonym in hyperonyms:
        if (hyperonym in not_to_db and isinstance(argvalue, (int, float, complex))) or \
            R.isRelBetween('hyperonym', hyperonym, argvalue): return True
    return False


def convert_by_argtable(fasif, argname, argvalue):
    if argvalue not in fasif['argdescr'][argname]['argtable']: return argvalue
    return fasif['argdescr'][argname]['argtable'][argvalue]


def check_args(finded_args, fasif, R):
    # Проверка на наличие в абстрактной группе
    hyperonyms = {}
    for argname, data in fasif['argdescr'].items():
        # пока только основные гиперонимы вытягиваем
        hyperonyms[argname] = [word['base'] for word in data['hyperonyms']]
    for finded_arg in finded_args:
        for argname, argvalue in list(finded_arg.items()):
            if not is_in_hyperonym(hyperonyms[argname], argvalue, R): del finded_arg[argname]

    # Проверка на отсутствие обязательных аргументных слов
    checked_args = []
    for finded_arg in finded_args:
        isright = True
        for argname, argdescr in fasif['argdescr'].items():
            if argname not in finded_arg and argdescr['isreq']:  # если отсутствует обязательный аргумент
                isright = False
                break
        if isright: checked_args.append(finded_arg)

    # Конвертирование аргументных слов по таблице из фасифа
    for checked_arg in checked_args:
        for argname, argvalue in checked_arg.items():
            checked_arg[argname] = convert_by_argtable(fasif, argname, argvalue)
    return checked_args


def il_build_func_value(fasif, type_func, verb_id_group=None, check_verb=False, try_antonym=True):
    """

    :param fasif:
    :param type_func:
    :param verb_id_group:
    :param check_verb:
    :param try_antonym:
    :return: (Данные функции, найдена ли финкция по антониму)
    """
    data_func = fasif['functions'].get(type_func)
    if data_func and check_verb:
        if verb_id_group not in data_func['verbs']:
            if try_antonym:
                # TODO: добавить антонимы для примера через глагол-связку. Здесь затем искать по id группы антонимов
                # verb_synonym_group_id = R.R.get_words_from_samegroup('antonym', 'verb', 'synonym', id_group)
                id_antonym = verb_id_group
                if id_antonym not in data_func['verbs']:
                    return data_func, True

            return False

    return data_func, False


def il_build_word_combination(data_get_value, data_set_value, finded_args, fasif, R):
    for argname, args in finded_args.items():
        finded_args[argname] = list(args)  # TODO: #UNIQ_ARGS Нужны ли нам дубли аргументов?

    finded_args = dproduct(finded_args)
    finded_args = check_args(finded_args, fasif, R)

    word_combination = {
        'func_get_value': importer.action(data_get_value['function']) if data_get_value else None,
        'func_set_value': importer.action(data_set_value['function']) if data_set_value else None,
        'arguments': finded_args,
        'how_put_args': fasif['args_as_list'],
    }
    return word_combination


def Extraction2IL(R, settings, subjects, predicate, arguments):
    fdb = finder.FasifDB(settings.c, settings.cu)
    verb = {'func_common': None, 'used_antonym': False, 'answer_type': settings.answer_type}
    internal_sentence = {
        'type_sentence': 'fact',
        'verb': verb,
        'word_combinations': [],
        'subjects_word_combinations': []
    }

    # определяем тип предложения

    if predicate['mood'] == 'imperative':
        internal_sentence['type_sentence'] = 'run'
    elif predicate['mood'] == 'indicative' and predicate['tense'] == 'present':
        internal_sentence['type_sentence'] = 'fact'

    #  Вынимаем ФАСИФ глагола - сказуемого

    id_group = R.R.get_groups_by_word('synonym', 0, predicate['base'], 'verb')
    id_group = id_group[0] if id_group else None
    if id_group is not None:
        compared_fasifs = fdb.getFASIF('Verb', id_group)
        if compared_fasifs:
            verb['func_common'] = importer.action(compared_fasifs[0][0][0])
        else:
            # TODO: проверить антоним (), как для функции изменения состояния
            pass

    # Вынимаем Фасиф словосочетаний - актантов
    for _argument in arguments:  # у подпредложения может быть несколько актантов
        argument = Sentence(_argument)
        compared_fasifs = fdb.getFASIF('WordCombination', argument)
        if compared_fasifs:
            finded_args, fasif = compared_fasifs[0]  # если фасифов несколько, то необходимо отсеть лишние в этом месте (отдельной функцией)

            # Вынимаем функцию получения/изменения состояния.

            verb['used_antonym'] = predicate['antonym']
            data_get_value, finded_by_antonym = il_build_func_value(fasif, 'getCondition')
            data_set_value, finded_by_antonym = il_build_func_value(fasif, 'changeCondition', id_group, check_verb=True)
            if finded_by_antonym:
                verb['used_antonym'] = not verb['used_antonym']

            word_combination = il_build_word_combination(data_get_value, data_set_value, finded_args, fasif, R)
            internal_sentence['word_combinations'].append(word_combination)

    # Вынимаем Фасиф словосочетаний - субъектов
    for _subject in subjects:
        subject = Sentence(_subject)
        compared_fasifs = fdb.getFASIF('WordCombination', subject)
        if compared_fasifs:
            finded_args, fasif = compared_fasifs[0]  # если фасифов несколько, то необходимо отсеть лишние в этом месте (отдельной функцией)

            # Вынимаем функцию получения состояния.

            verb['used_antonym'] = predicate['antonym']
            data_get_value, finded_by_antonym = il_build_func_value(fasif, 'getCondition')
            word_combination = il_build_word_combination(data_get_value, None, finded_args, fasif, R)
            internal_sentence['subjects_word_combinations'].append(word_combination)

    #with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
    #    flog.write('\npraIL: %s\n' % str(internal_sentence))

    return internal_sentence


def convert(sentences, OR, settings):
    internal_sentences = {}
    # перебираем предложения
    il_index = 0
    for sentence in sentences:
        subjects_by_predicate, predicates, arguments_by_predicate = sentence
        # перебираем однородные, придаточные и главные подпредложения
        for subjects, predicate, arguments in zip(subjects_by_predicate, predicates, arguments_by_predicate):
            internal_sentences[il_index] = Extraction2IL(OR, settings, subjects, predicate, arguments)
            il_index += 1
    return internal_sentences
