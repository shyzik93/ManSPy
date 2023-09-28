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
    return [dict(i) for i in l]


def is_in_hyperonym(hyperonyms, argvalue, relation):
    is_argvalue_integer = isinstance(argvalue, (int, float, complex))
    for hyperonym_word in hyperonyms:
        hyperonym = hyperonym_word['unit_info']['base']
        if (hyperonym in not_to_db and is_argvalue_integer) or relation.is_rel_between('hyperonym', hyperonym, argvalue):
            return True


def filter_and_convert_args(finded_vargs, argsdescr, relation):
    req_argnames = {argname for argname, argdescr in argsdescr.items() if argdescr['isreq']}
    for finded_varg in finded_vargs:
        # Фильтруем по наличию в абстрактной группе
        for argname, argvalue in list(finded_varg.items()):
            if not is_in_hyperonym(argsdescr[argname]['hyperonyms'], argvalue, relation):
                del finded_varg[argname]

        # Фильтруем по отсутствию обязательных аргументных слов
        if req_argnames <= set(finded_varg.keys()):
            # Конвертируем аргументные слова по таблице из фасифа
            for argname, argvalue in finded_varg.items():
                finded_varg[argname] = argsdescr[argname]['argtable'].get(argvalue, argvalue)

            yield finded_varg


def get_func_common(relation, base, settings):
    id_group = relation.get_groups_by_word('synonym', 0, base)
    id_group = id_group[0] if id_group else None
    if id_group is not None:
        compared_fasifs = find(settings, 'verb', id_group)
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


def get_func_wcomb(argument, settings, relation, verb_id_group):
    compared_fasifs = find(settings, 'word_combination', argument)
    if compared_fasifs:
        finded_args, fasif = compared_fasifs[0]  # если фасифов несколько, то необходимо отсеть лишние в этом месте (отдельной функцией)
        finded_args = dproduct(finded_args)
        finded_args = list(filter_and_convert_args(finded_args, fasif['argdescr'][settings.language], relation))

        # Вынимаем функцию получения/изменения состояния.

        data_get_value = fasif['functions'].get('getCondition')
        data_set_value = fasif['functions'].get('changeCondition')
        finded_set_by_antonym = il_build_func_value(data_set_value, settings.language, verb_id_group, check_verb=True)
        return (
            data_get_value['function'] if data_get_value else None,
            data_set_value['function'] if data_set_value else None,
            finded_args,
            finded_set_by_antonym,
        )

    return None, None, None, None
