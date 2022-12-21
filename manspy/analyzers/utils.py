from manspy.storage.fasif.finder import find


def get_func_common(relation, verb_id_group, settings):
    id_group = relation.get_groups_by_word('synonym', 0, verb_id_group)
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
                # verb_synonym_group_id = R.R.get_words_from_samegroup('antonym', 'verb', 'synonym', id_group)
                id_antonym = verb_id_group
                if id_antonym not in data_func['verbs'][language]:
                    return True

    return False


def get_func_wcomb_for_arguments(argument, settings, verb_id_group):
    compared_fasifs = find(settings, 'word_combination', argument, settings.language)
    if compared_fasifs:
        finded_args, fasif = compared_fasifs[0]  # если фасифов несколько, то необходимо отсеть лишние в этом месте (отдельной функцией)

        # Вынимаем функцию получения/изменения состояния.

        data_get_value = fasif['functions'].get('getCondition')
        finded_get_by_antonym = il_build_func_value(data_get_value, settings.language)
        data_set_value = fasif['functions'].get('changeCondition')
        finded_set_by_antonym = il_build_func_value(data_set_value, settings.language, verb_id_group, check_verb=True)
        return data_get_value, data_set_value, finded_args, fasif, finded_set_by_antonym

    return None, None, None, None, None


def get_func_wcomb_for_subjects(subject, settings):
    compared_fasifs = find(settings, 'word_combination', subject, settings.language)
    if compared_fasifs:
        finded_args, fasif = compared_fasifs[0]  # если фасифов несколько, то необходимо отсеть лишние в этом месте (отдельной функцией)

        # Вынимаем функцию получения состояния.

        data_get_value = fasif['functions'].get('getCondition')
        _ = il_build_func_value(data_get_value, settings.language)
        return data_get_value, finded_args, fasif

    return None, None, None
