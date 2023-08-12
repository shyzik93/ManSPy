import itertools

from manspy.storage.fasif.finder import find

not_to_db = ['nombr', 'cifer']  # TODO:  существует ещё одна переменная с таким же именем. Нужно сделать общий источник


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


def is_in_hyperonym(hyperonyms, argvalue, relation):
    for hyperonym in hyperonyms:
        if (hyperonym in not_to_db and isinstance(argvalue, (int, float, complex))) or \
                relation.isRelBetween('hyperonym', hyperonym, argvalue):
            return True

    return False


def convert_by_argtable(argdescr, argname, argvalue):
    if argvalue not in argdescr[argname]['argtable']:
        return argvalue

    return argdescr[argname]['argtable'][argvalue]


def check_args(finded_args, fasif, relation, language):
    # Проверка на наличие в абстрактной группе
    hyperonyms = {}
    for argname, data in fasif['argdescr'][language].items():
        # пока только основные гиперонимы вытягиваем
        hyperonyms[argname] = [word['unit_info']['base'] for word in data['hyperonyms']]
    for finded_arg in finded_args:
        for argname, argvalue in list(finded_arg.items()):
            if not is_in_hyperonym(hyperonyms[argname], argvalue, relation):
                del finded_arg[argname]

    # Проверка на отсутствие обязательных аргументных слов
    checked_args = []
    for finded_arg in finded_args:
        isright = True
        for argname, argdescr in fasif['argdescr'][language].items():
            if argname not in finded_arg and argdescr['isreq']:  # если отсутствует обязательный аргумент
                isright = False
                break

        if isright:
            checked_args.append(finded_arg)

    # Конвертирование аргументных слов по таблице из фасифа
    for checked_arg in checked_args:
        for argname, argvalue in checked_arg.items():
            # TODO: раскрыть функцию convert_by_argtable
            checked_arg[argname] = convert_by_argtable(fasif['argdescr'][language], argname, argvalue)

    return checked_args


def get_func_common(relation, base, settings):
    id_group = relation.get_groups_by_word('synonym', 0, base)
    id_group = id_group[0] if id_group else None
    if id_group is not None:
        compared_fasifs = find(settings, 'verb', id_group, settings.language)
        if compared_fasifs:
            return id_group, compared_fasifs[0][0][0]
        else:
            # TODO: проверить антоним (), как для функции изменения состояния
            pass

    return id_group, None


def il_build_func_value(data_func, language, verb_id_group=None, check_verb=False, try_antonym=True):
    """

    :param data_func:
    :param language:
    :param verb_id_group:
    :param check_verb:
    :param try_antonym:
    :return: найдена ли финкция по антониму
    """
    if data_func and check_verb:
        if verb_id_group not in data_func['verbs'][language]:
            if try_antonym:
                # TODO: добавить антонимы для примера через глагол-связку. Здесь затем искать по id группы антонимов
                # verb_synonym_group_id = R.R.get_words_from_samegroup('antonym', VERB, 'synonym', id_group)
                id_antonym = verb_id_group
                if id_antonym not in data_func['verbs'][language]:
                    return True

    return False


def get_func_wcomb(argument, settings, relation, verb_id_group):
    compared_fasifs = find(settings, 'word_combination', argument, settings.language)
    if compared_fasifs:
        finded_args, fasif = compared_fasifs[0]  # если фасифов несколько, то необходимо отсеть лишние в этом месте (отдельной функцией)
        finded_args = dproduct(finded_args)
        finded_args = check_args(finded_args, fasif, relation, settings.language)

        # Вынимаем функцию получения/изменения состояния.

        data_get_value = fasif['functions'].get('getCondition')
        finded_get_by_antonym = il_build_func_value(data_get_value, settings.language)
        data_set_value = fasif['functions'].get('changeCondition')
        finded_set_by_antonym = il_build_func_value(data_set_value, settings.language, verb_id_group, check_verb=True)
        return (
            data_get_value['function'] if data_get_value else None,
            data_set_value['function'] if data_set_value else None,
            finded_args,
            finded_set_by_antonym,
        )

    return None, None, None, None
