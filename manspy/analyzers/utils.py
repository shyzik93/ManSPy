from manspy.storage.fasif.finder import find


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
