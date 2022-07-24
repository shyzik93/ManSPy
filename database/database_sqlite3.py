import json
import sqlite3


class FasifDB:
    def __init__(self, c, cu):
        self.c, self.cu = c, cu
        self.cu.execute('''
            CREATE TABLE IF NOT EXISTS fasifs (
                id_fasif INTEGER PRIMARY KEY AUTOINCREMENT,
                type_fasif TEXT,
                fasif TEXT UNIQUE ON CONFLICT IGNORE
        );''')

    def safe(self, type_fasif, fasif):
        self.cu.execute(
            'INSERT INTO fasifs (type_fasif, fasif) VALUES (?,?)',
            (type_fasif, json.dumps(fasif, sort_keys=True))
        )
        self.c.commit()

    def get(self, type_fasif):
        rows = self.cu.execute('SELECT fasif FROM fasifs WHERE type_fasif=?', (type_fasif,))
        for row in rows:
            yield json.loads(row['fasif'])


class Relation:
    dct_speeches = {'noun': 1, 'verb': 2, 'adjective': 3, 'adverb': 4}

    def __init__(self, c, cu):
        self.c, self.cu = c, cu
        self.cu.executescript('''
                    CREATE TABLE IF NOT EXISTS words (
                      word TEXT COLLATE NOCASE UNIQUE ON CONFLICT IGNORE,
                      id_word INTEGER PRIMARY KEY);
                    CREATE TABLE IF NOT EXISTS relations (
                      id_type INTEGER,
                      id_speech INTEGER,
                      id_group INTEGER,
                      id_word INTEGER,
                      isword INTEGER );
                    CREATE TABLE IF NOT EXISTS descr_relation (
                      id_relation INTEGER PRIMARY KEY,
                      type_relation TEXT,
                      count_members INTEGER,
                      type_parent TEXT, -- тип вершины (группы)
                      type_child TEXT, -- тип членов
                      name1 TEXT COLLATE NOCASE UNIQUE ON CONFLICT IGNORE,
                      name2 TEXT COLLATE NOCASE);''')
        # name2 - для иерархических отношений.
        # В иерархических отношениях name1 обозначает вышестоящий объект, name2 - нижестоящий.
        # В линейных отношениях оба объекта равны, => для обеих обеих объектов используется одно название - name1
        self.dct_speechesR = {}
        for k, v in self.dct_speeches.items():
            self.dct_speechesR[v] = k

    def _type2id(self, relation):
        if not isinstance(relation, str): return relation
        res = self.cu.execute('SELECT id_relation FROM descr_relation WHERE name1=?;', (relation,)).fetchall()
        if res: return res[0][0]
        #return self.dct_types[_type] if isinstance(_type, (str, unicode)) else _type

    def _speech2id(self, speech): return self.dct_speeches[speech] if isinstance(speech, str) else speech

    def add_word(self, *words):
        self.cu.execute(
            'INSERT INTO words (word) VALUES '+','.join(['(?)' for word in words])+';',
            [word.lower() for word in words]
        )
        self.c.commit()

    ### Работа с таблицей words

    def _word2id(self, word):
        if not isinstance(word, str): return word
        res = self.cu.execute('SELECT id_word FROM words WHERE word=?;', (word,)).fetchall()
        if res: return res[0][0]
        else: # если слово отсутствует, то добавим его
            self.add_word(word)
            return self._word2id(word)

    ### Работа с таблицей relations

    def get_max_id(self, name, id_type=None):
        if id_type == None: res = self.cu.execute('SELECT MAX(%s) FROM relations;'%name).fetchall()[0][0]
        else: res = self.cu.execute('SELECT MAX(%s) FROM relations WHERE id_type=?;'%name, (id_type, )).fetchall()[0][0]
        return res if res != None else 0

    def check_copy_row(self, id_type, id_speech, id_group, id_word, isword, _exists):
        if id_speech != None: id_speech = self._speech2id(id_speech)
        #else: id_speech = 'NULL'
        # если id_speech = None, то база это не считает за NULL. Это нужно исправить и раскомментировать три строки
        groups = False
        if self._type2id(id_type) in [3]:
            #groups = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_speech=? AND id_group=? AND id_word=? AND isword=?',
            #                (self._type2id(id_type), id_speech, self._word2id(id_group), self._word2id(id_word), self._type2id(isword))).fetchall()
            groups = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_group=? AND id_word=? AND isword=?',
                            (self._type2id(id_type), self._word2id(id_group), self._word2id(id_word), self._type2id(isword))).fetchall()
        elif self._type2id(id_type) in [1,2]:
            if _exists != None:
                groups = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_speech=? AND id_group=? AND id_word=? AND isword=?',
                            (self._type2id(id_type), id_speech, self._word2id(id_group), self._word2id(id_word), self._type2id(isword))).fetchall()
            else:
                groups = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_speech=? AND id_word=? AND isword=?',
                          (self._type2id(id_type), id_speech, self._word2id(id_word), self._type2id(isword))).fetchall()
        return [_id[0] for _id in groups] if groups else False


class Database:
    def __init__(self, database_settings):
        sqlite3.enable_callback_tracebacks(True)
        self.c = sqlite3.connect(database_settings['path'])
        self.c.row_factory = sqlite3.Row
        self.cu = self.c.cursor()

        self.fasif = FasifDB(self.c, self.cu)
        self.relation = Relation(self.c, self.cu)

    def __enter__(self, database_settings):
        sqlite3.enable_callback_tracebacks(True)
        self.c = sqlite3.connect(database_settings['path'])
        self.c.row_factory = sqlite3.Row
        self.cu = self.c.cursor()

    def __exit__(self, Type, Value, Trace):
        self.c.close()

    def close(self):
        self.c.close()

    def get_fasif(self, type_fasif):
        return self.fasif.get(type_fasif)

    def save_fasif(self, type_fasif, fasif):
        self.fasif.safe(type_fasif, fasif)

    def convert(self, *inlist):
        ''' Преобразовывает id в слово или слово в id '''
        outlist = []
        for el in inlist:
            if isinstance(el, int):
                query = 'SELECT word FROM words WHERE id_word=?;'
            else:
                query = 'SELECT id_word FROM words WHERE word=?;'
            res = self.cu.execute(query, (el,)).fetchall()
            if res:
                outlist.append(res[0][0])
            else: # если слово отсутствует, то добавим его
                self.relation.add_word(el)
                outlist.append(*convert(el))
        return outlist

    def word2id(self, word):
        return self.relation._word2id(word)

    # Работа с таблицей relations

    def add_words2group(self, id_type, id_speech, id_group, isword, *id_words):
        ''' Добавляет слова в существующую группу.
            Если id_group = None, то создастся новая группа'''
        id_groups = []
        _exists = id_group
        if id_group is None:
            id_group = self.relation.get_max_id('id_group', self.relation._type2id(id_type)) + 1
        for id_word in id_words:
            _id_group = self.relation.check_copy_row(id_type, id_speech, id_group, id_word, isword, _exists)
            if _id_group is False:
                self.cu.execute('INSERT INTO relations (id_type, id_speech, id_group, id_word, isword) VALUES (?,?,?,?,?);',
                            (self.relation._type2id(id_type), self.relation._speech2id(id_speech), self.relation._word2id(id_group), self.relation._word2id(id_word), self.relation._type2id(isword)))
                id_groups.append(id_group)
            else:
                id_groups.append(_id_group)
        self.c.commit()
        return id_group

    def get_groups_by_word(self, id_type, isword, id_word, id_speech=None):
        ''' Возвращает группы, в которые входит слово '''
        if id_speech != None:
            res = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_speech=? AND id_word=? AND isword=?',
                          (self.relation._type2id(id_type), self.relation._speech2id(id_speech), self.relation._word2id(id_word), self.relation._type2id(isword))).fetchall()
        else:
            res = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_word=? AND isword=?',
                          (self.relation._type2id(id_type), self.relation._word2id(id_word), self.relation._type2id(isword))).fetchall()
        return [_id[0] for _id in res]

    def get_words_by_group(self, id_type, id_group, isword, id_speech=None):
        ''' Возвращает слова, входящие в группу '''
        if id_speech != None:
            res = self.cu.execute('SELECT id_word FROM relations WHERE id_type=? AND id_speech=? AND id_group=? AND isword=?;',
                          (self.relation._type2id(id_type), self.relation._speech2id(id_speech), self.relation._word2id(id_group), self.relation._type2id(isword))).fetchall()
        else:
            res = self.cu.execute('SELECT id_word FROM relations WHERE id_type=? AND id_group=? AND isword=?',
                          (self.relation._type2id(id_type), self.relation._word2id(id_group), self.relation._type2id(isword))).fetchall()
        return [_id[0] for _id in res]

    # Работа с таблицей descr_relation

    def add_descr_relation(self, **descr):
        self.cu.execute("INSERT INTO descr_relation (count_members, type_relation, name1, name2) VALUES (?,?,?,?)" , (descr['count_members'],descr['type_relation'], descr['name1'], descr['name2']))
        self.c.commit()

    def get_descr_relation(self, relation=None):
        if relation is not None:
            #name = 'name1' if isinstance(relation, (str, unicode)) else 'id_relation'
            #descr = self.cu.execute("SELECT * FROM descr_relation WHERE "+name+"=?", (relation,)).fetchall()
            if isinstance(relation, str): descr = self.cu.execute("SELECT * FROM descr_relation WHERE name1=? OR name2=?", (relation,relation)).fetchall()
            else: descr = self.cu.execute("SELECT * FROM descr_relation WHERE id_relation=?", (relation,)).fetchall()
            descr = [dict(row) for row in descr]
            return descr[0] if descr else {}
        else:
            descr = self.cu.execute("SELECT * FROM descr_relation").fetchall()
            descr = [dict(row) for row in descr]
            return descr if descr else []