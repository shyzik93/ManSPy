from typing import List, Optional, Union

from manspy.utils.unit import Word


class Relation:
    """ Надкласс, реализующий высокий уровень работы с разными группами слов, абстрагируясь от БД.
        Другими словами, он задествует вышеуказанные классы для реализации своих
        функций."""
    INFINITY = 0

    def __init__(self, settings):
        self.db = settings.database

    ### Составные функции для таблицы relations (работают с идентификаторами)

    def add_words2samegroup(self, id_type, id_speech, isword, id_word, *id_words):
        ''' Добавляет все id_words в ту группу, в которой находится id_word.
            Если id_word не входит ни в одну группу, то оно добавится в новую группу'''
        id_groups = self.db.get_groups_by_word(id_type, isword, id_word, id_speech)
        if not id_groups:
            self.db.add_words2group(id_type, id_speech, None, isword, id_word)
            id_groups = self.db.get_groups_by_word(id_type, id_speech, isword, id_word)
        for id_group in id_groups:
            self.db.add_words2group(id_type, id_speech, id_group, isword, *id_words)

    def get_words_from_samegroup(self, id_type, id_speech, isword, id_word):
        ''' Возвращает слова из той группы, в которую входит id_word ''' #работает медленно
        id_groups = self.db.get_groups_by_word(id_type, isword, id_word, id_speech)
        id_words = []
        for id_group in id_groups:
            res = self.db.get_words_by_group(id_type, id_group, isword, id_speech)
            if res: id_words.extend(res)
        return list(set(id_words))

    def is_word_in_group(self, id_type, id_group, id_word, isword, id_speech=None):
        ''' Входит ли слово в группу? '''
        id_words = self.db.get_words_by_group(id_type, id_group, isword, id_speech)
        return self.db.word2id(id_word) in id_words

    def get_commongroups(self, id_type, id_speech, *pairs):
        ''' Возвращает общие для всех слов группы '''
        # pair = [id_word, isword]
        list_groups = []
        for pair in pairs:
            list_groups.append(self.db.get_groups_by_word(id_type, pair[1], pair[0], id_speech))

        common_id_groups = set(list_groups.pop(0))
        for list_group in list_groups:
            common_id_groups &= set(list_group)
        return list(common_id_groups)

    def get_groups_by_word(self, id_type, isword, id_word, id_speech=None):
        return self.db.get_groups_by_word(id_type, isword, id_word, id_speech)

    def is_rel_between(self, relation, *words):
        ''' Is the relation 'relation' between word1 and word2 ?
        Являются ли слова word1 и word2 relation'ами (синониами, антонимаими, гиперонимом и гипонимом соответственно, холонимом и меронимом соответственно) ?
        '''
        if isinstance(relation, dict):
            descr = relation
            relation = relation['id_relation']
        else:
            descr = self.db.get_descr_relation(relation)

        if descr['type_relation'] == 'line':
            _words = [[word, 0] for word in words]
            return bool(self.get_commongroups(relation, None, *words))
        elif descr['type_relation'] == 'tree':
            if len(words) < 2:
                raise Exception('count words must be 2 or more')

            source_word = words[0]
            for word in words[1:]:
                if not self.is_word_in_group(relation, source_word, word, 0, None):
                    return False

            return True

    def _isAnyRelBetween(self, word1, word2):
        ''' Is any relation 'relation' between word1 and word2 ?
            Есть ли какие-либо отношения между словами word1 и word2 ?
        '''
        relations = []
        descrs = self.db.get_all_descr_relations()
        for descr in descrs:
            relation = descr['id_relation']
            if self.is_rel_between(relation, word1, word2):
                relations.append(relation)

        return relations

    def _whomRelBetween(self, relation, word1):
      ''' With whom does word1 has relation
      '''
      pass

    def _whatRelBetween(self, word1, word2):
      ''' what relation or relations are between word1 and word2 ?
      '''
      pass

    def _getRelation(self, relation, word1, word2=None):
        ''' Первое слово для иерархиских отношений должно быть выше уровня  '''
        if relation:
            descr = self.db.get_descr_relation(relation)

        if word1 and word2:
            if relation: # Is the relation between word1 and word2 ?
                return self.is_rel_between(relation, word1, word2)
            else: # Is any relation between word1 and word2 ?
                pass

        elif word1 and not word2:
            if relation: # With who does word1 have the relation ?
                pass
            else: # With who does word1 have any relation ?
                pass

    # Временные функции-обёртки, для понимания задачи.
    def isAnyRelBetween(self, word1, words2):
        ''' Is any relation 'relation' between word1 and word2 ?
            Есть ли какие-либо отношения между словами word1 и word2 ?
            @return bool
        '''
        pass

    def whatRelBetween(self, word1, word2):
        ''' what relation or relations are between word1 and word2 ?
            @return list of relations
        '''
        pass

    def whomRelBetween(self, relation, word1):
        ''' With whom does word1 has relation
            @return list of words
        '''
        if relation == 'synonym':
            return self.db.convert(self.get_words_from_samegroup('synonym', None, 0, word1))

        elif relation == 'antonym':
            syn_groups = self.db.get_groups_by_word('synonym', 0, word1, None)
            if not syn_groups:
                return []

            syn_groups = self.get_words_from_samegroup('antonym', None, self.dct_types['synonym'], syn_groups[0])
            if not syn_groups:
                return []

            return self.db.convert(self.db.get_words_by_group('synonym', syn_group, 0, None))

    def set_relation(self, type_relation: str, group: Optional[Union[int, Word]], *members: List[Union[int, Word]]) -> int:
        """
        Устанавливает новое отношение между членами либо добавляет членов к существующему отношению
        :param type_relation: тип отношения
        :param group: существующая группа, в которую будут добавлены члены. Равно `None`, если для членов нужно создать новую группу.
        :param members: члены
        :return: идентификатор существующей либо новой группы
        """
        group = group['base'] if isinstance(group, Word) else group
        members = [word['base'] for word in list(members)]

        descr = self.db.get_descr_relation(type_relation)
        if descr['count_members'] != self.INFINITY:
            if len(members) != descr['count_members']:
                raise Exception('This relation have to have {} members max'.format(descr['count_members']))

        if descr['type_group'] == 'index' and group is None:
            group = self.db.get_new_index()
        elif descr['type_group'] == 'word' and group is None:
            raise Exception('You have to point the group, if the type of group is "word"')

        return self.db.add_words2group(type_relation, None, group, 0, *members)
