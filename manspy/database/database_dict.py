from typing import Optional, Union

from manspy.utils.constants import ADJECTIVE, ADVERB, NOUN, VERB


class Database:
    dct_speeches = {NOUN: 1, VERB: 2, ADJECTIVE: 3, ADVERB: 4}
    fasifs = {}
    word_by_id = {}
    id_by_word = {}
    max_group_index = 0
    max_word_id = 0
    descr_relation = {}
    id_descr_relation_by_member_names = {}
    id_descr_relation_by_group_names = {}

    def __init__(self, database_settings):
        pass

    def close(self):
        pass

    def get_fasif(self, type_fasif):
        return self.fasifs.get(type_fasif, [])

    def save_fasif(self, type_fasif, fasif):
        fasifs = self.fasifs.setdefault(type_fasif, [])
        fasifs.append(fasif)

    def _speech2id(self, speech: Optional[Union[str, int]]) -> int:
        return self.dct_speeches[speech] if isinstance(speech, str) else speech

    def get_new_index(self):
        self.max_group_index += 1
        return self.max_group_index

    # Работа с таблицей words

    def add_word(self, *words: str) -> int:
        for word in words:
            self.max_word_id += 1
            word = word.lower()
            self.word_by_id[self.max_word_id] = word
            self.id_by_word[word] = self.max_word_id

        return self.max_word_id

    def word2id(self, word: str) -> int:
        if isinstance(word, int):
            return word

        word_id = self.id_by_word.get(word)
        return word_id if word_id else self.add_word(word)

    def convert(self, *inlist):
        ''' Преобразовывает id в слово или слово в id '''
        for el in inlist:
            if isinstance(el, int):
                word = self.word_by_id.get(el)
                if not word:
                    raise Exception(f'Word with id {el} not found')
                yield word
            else:
                word_id = self.id_by_word.get(el)
                yield word_id if word_id else self.add_word(el)

    # Работа с таблицей descr_relation

    def _type2id(self, name_for_member: Union[str, int]) -> int:
        if not isinstance(name_for_member, str):
            return name_for_member

        return self.id_descr_relation_by_member_names[name_for_member]

    def add_descr_relation(self, type_relation: str, count_members: int, type_member: str, name_for_member: str, name_for_group: str):
        # type_member - пока определяется на основании `relations.member_is_word`
        if type_relation == 'line':
            type_group = 'index'
        elif type_relation == 'tree':
            type_group = 'word'
        else:
            raise Exception('unknown `type_relation`')

        id_descr = len(self.descr_relation)
        self.descr_relation[id_descr] = {
            'count_members': count_members,
            'type_relation': type_relation,
            'type_group': type_group,
            'name_for_member': name_for_member,
            'name_for_group': name_for_group,
        }
        self.id_descr_relation_by_group_names[name_for_group] = id_descr
        self.id_descr_relation_by_member_names[name_for_member] = id_descr

    def get_descr_relation(self, relation: Union[int, str]):
        if isinstance(relation, str):
            id_descr = (
                self.id_descr_relation_by_member_names.get(relation)
                or self.id_descr_relation_by_group_names.get(relation)
            )
        else:
            id_descr = relation

        return self.descr_relation[id_descr]

    def get_all_descr_relations(self):
        return self.descr_relation.values()

    # Работа с таблицей relations
