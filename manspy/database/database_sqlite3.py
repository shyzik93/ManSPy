import json
import sqlite3
from typing import Optional, Union

from manspy.utils.constants import ADJECTIVE, ADVERB, NOUN, VERB


class Database:
    SQL_INSERT_DESCR_RELATION = (
        'INSERT INTO descr_relation (count_members, type_relation, type_group, name_for_member, name_for_group) VALUES (?,?,?,?,?)'
    )
    dct_speeches = {NOUN: 1, VERB: 2, ADJECTIVE: 3, ADVERB: 4}
    c = None
    cu = None

    def __init__(self, database_settings):
        sqlite3.enable_callback_tracebacks(True)
        if not self.c:
            self.c = sqlite3.connect(database_settings['path'])
            self.c.row_factory = sqlite3.Row
            self.cu = self.c.cursor()

            self.cu.executescript("""
                CREATE TABLE IF NOT EXISTS fasifs (
                  id_fasif INTEGER PRIMARY KEY AUTOINCREMENT,
                  type_fasif TEXT,
                  fasif TEXT UNIQUE ON CONFLICT IGNORE);
                CREATE TABLE IF NOT EXISTS words (
                  word TEXT COLLATE NOCASE UNIQUE ON CONFLICT IGNORE,
                  id_word INTEGER PRIMARY KEY);
                CREATE TABLE IF NOT EXISTS max_index (
                  group_index INTEGER);
                CREATE TABLE IF NOT EXISTS relations (
                  id_descr_relation INTEGER,
                  id_speech INTEGER,
                  id_group INTEGER,
                  id_member INTEGER,
                  member_is_word INTEGER );
                CREATE TABLE IF NOT EXISTS descr_relation (
                  id_descr_relation INTEGER PRIMARY KEY,
                  type_relation TEXT, -- tree или line
                  count_members INTEGER,
                  type_group TEXT, -- тип вершины (группы)
                  type_member TEXT, -- тип членов
                  name_for_member TEXT COLLATE NOCASE UNIQUE ON CONFLICT IGNORE,
                  name_for_group TEXT COLLATE NOCASE);
            """)

    def close(self):
        self.c.close()

    def get_fasif(self, type_fasif):
        rows = self.cu.execute('SELECT fasif FROM fasifs WHERE type_fasif=?', (type_fasif,))
        for row in rows:
            yield json.loads(row['fasif'])

    def save_fasif(self, type_fasif, fasif):
        self.cu.execute(
            'INSERT INTO fasifs (type_fasif, fasif) VALUES (?,?)',
            (type_fasif, json.dumps(fasif, sort_keys=True))
        )
        self.c.commit()

    def _speech2id(self, speech: Optional[Union[str, int]]) -> int:
        return self.dct_speeches[speech] if isinstance(speech, str) else speech

    def get_new_index(self):
        index = self.cu.execute('SELECT group_index FROM max_index').fetchone()
        if index:
            index = index['group_index'] + 1
            self.cu.execute('UPDATE max_index SET group_index=?', (index,))
        else:
            index = 1
            self.cu.execute('INSERT INTO max_index VALUES (?)', (index,))

        self.c.commit()
        return index

    # Работа с таблицей words

    def add_word(self, *words: str) -> int:
        self.cu.execute(
            'INSERT INTO words (word) VALUES {};'.format(','.join('(?)' for _ in words)),
            [word.lower() for word in words]
        )
        self.c.commit()
        return self.cu.lastrowid

    def word2id(self, word: str) -> int:
        if isinstance(word, int):
            return word

        res = self.cu.execute('SELECT id_word FROM words WHERE word=?;', (word,)).fetchone()
        return res[0] if res else self.add_word(word)

    def convert(self, *inlist):
        ''' Преобразовывает id в слово или слово в id '''
        for el in inlist:
            if isinstance(el, int):
                query = 'SELECT word FROM words WHERE id_word=?;'
            else:
                query = 'SELECT id_word FROM words WHERE word=?;'

            res = self.cu.execute(query, (el,)).fetchall()
            yield res[0][0] if res else self.add_word(el)

    # Работа с таблицей descr_relation

    def _type2id(self, name_for_member: Union[str, int]) -> int:
        if not isinstance(name_for_member, str):
            return name_for_member

        res = self.cu.execute(
            'SELECT id_descr_relation FROM descr_relation WHERE name_for_member=?;',
            (name_for_member, )
        ).fetchall()
        if res:
            return res[0][0]

    def add_descr_relation(self, type_relation: str, count_members: int, type_member: str, name_for_member: str, name_for_group: str):
        # type_member - пока определяется на основании `relations.member_is_word`
        if type_relation == 'line':
            type_group = 'index'
        elif type_relation == 'tree':
            type_group = 'word'
        else:
            raise Exception('unknown `type_relation`')

        self.cu.execute(
            self.SQL_INSERT_DESCR_RELATION,
            (count_members, type_relation, type_group, name_for_member, name_for_group)
        )
        self.c.commit()

    def get_descr_relation(self, relation: Union[int, str]):
        if isinstance(relation, str):
            return self.cu.execute(
                'SELECT * FROM descr_relation WHERE name_for_member=? OR name_for_group=? limit 1',
                (relation, relation)
            ).fetchone()

        return self.cu.execute(
            'SELECT * FROM descr_relation WHERE id_descr_relation=? limit 1',
            (relation,)
        ).fetchone()

    def get_all_descr_relations(self):
        return self.cu.execute("SELECT * FROM descr_relation").fetchall()

    # Работа с таблицей relations

    def check_copy_row(self, id_type, id_speech, id_group, id_word, isword, _exists):
        id_speech = self._speech2id(id_speech)
        groups = False
        if self._type2id(id_type) in [3]:
            groups = self.cu.execute(
                'SELECT id_group FROM relations WHERE id_descr_relation=? AND id_group=? AND id_member=? AND member_is_word=?',
                (self._type2id(id_type), self.word2id(id_group), self.word2id(id_word), isword)
            ).fetchall()
        elif self._type2id(id_type) in [1, 2]:
            if _exists is None:
                groups = self.cu.execute(
                    'SELECT id_group FROM relations WHERE id_descr_relation=? AND id_speech=? AND id_member=? AND member_is_word=?',
                    (self._type2id(id_type), id_speech, self.word2id(id_word), isword)).fetchall()
            else:
                groups = self.cu.execute(
                    'SELECT id_group FROM relations WHERE id_descr_relation=? AND id_speech=? AND id_group=? AND id_member=? AND member_is_word=?',
                    (self._type2id(id_type), id_speech, self.word2id(id_group), self.word2id(id_word), isword)
                ).fetchall()

        return [_id[0] for _id in groups] if groups else False

    def add_words2group(self, id_type, id_speech, id_group, isword, *id_words):
        ''' Добавляет слова в существующую группу.
            Если id_group = None, то создастся новая группа'''
        id_groups = []
        for id_word in id_words:
            _id_group = self.check_copy_row(id_type, id_speech, id_group, id_word, isword, id_group)
            if _id_group:
                id_groups.append(_id_group)
            else:
                self.cu.execute(
                    'INSERT INTO relations (id_descr_relation, id_speech, id_group, id_member, member_is_word) VALUES (?,?,?,?,?);',
                    (
                        self._type2id(id_type),
                        self._speech2id(id_speech),
                        self.word2id(id_group),
                        self.word2id(id_word),
                        isword
                    )
                )
                id_groups.append(id_group)

        self.c.commit()
        return id_group

    def get_groups_by_word(self, id_type, isword, id_word, id_speech=None):
        ''' Возвращает группы, в которые входит слово '''
        if id_speech != None:
            res = self.cu.execute('SELECT id_group FROM relations WHERE id_descr_relation=? AND id_speech=? AND id_member=?',
                          (self._type2id(id_type), self._speech2id(id_speech), self.word2id(id_word))).fetchall()
        else:
            res = self.cu.execute('SELECT id_group FROM relations WHERE id_descr_relation=? AND id_member=?',
                          (self._type2id(id_type), self.word2id(id_word))).fetchall()
        return [_id[0] for _id in res]

    def get_words_by_group(self, id_type, id_group, isword, id_speech=None):
        ''' Возвращает слова, входящие в группу '''
        if id_speech is None:
            res = self.cu.execute(
                'SELECT id_member FROM relations WHERE id_descr_relation=? AND id_group=?',
                (self._type2id(id_type), self.word2id(id_group))
            ).fetchall()
        else:
            res = self.cu.execute(
                'SELECT id_member FROM relations WHERE id_descr_relation=? AND id_speech=? AND id_group=?;',
                (
                    self._type2id(id_type),
                    self._speech2id(id_speech),
                    self.word2id(id_group)
                )
            ).fetchall()

        return [_id[0] for _id in res]
