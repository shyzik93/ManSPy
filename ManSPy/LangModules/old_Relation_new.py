# -*- coding: utf-8 -*-
import sqlite3 as sql, os, pickle

def create_bd_file(language, name):
  if __name__ == '__main__': db_dir = 'F:\\SourceCode\\DATA_BASE'
  else: db_dir = os.path.abspath('DATA_BASE')
  if not os.path.exists(db_dir) or not os.path.isdir(db_dir):
    os.mkdir(db_dir)
  db_dir = os.path.join(db_dir, language)
  if not os.path.exists(db_dir) or not os.path.isdir(db_dir):
    os.mkdir(db_dir)
  name = os.path.join(db_dir, name)
  c = sql.connect(name)
  cu = c.cursor()
  return c, cu

class _Relation():
  def __init__(self, language):
    self.c, self.cu = create_bd_file(language, 'words.db')
    print dir(self.cu)
    self.cu.executescript('''
      CREATE TABLE IF NOT EXISTS words (
        word TEXT COLLATE NOCASE UNIQUE ON CONFLICT IGNORE,
        id_word INTEGER PRIMARY KEY);
      CREATE TABLE IF NOT EXISTS relations (
        id_type INTEGER,
        id_speech INTEGER,
        id_group INTEGER,
        id_word INTEGER,
        isword INTEGER );''')

  # Работа с таблицей words
  def add_word(self, *words):
    for word in words:
      self.cu.execute('INSERT INTO words (word) VALUES (?)', (word.lower(),))
    self.c.commit()
  def _id_to_word(self, _id):
    res = self.cu.execute('SELECT word FROM words WHERE id_word=?', (_id,)).fetchall()
    if res: return res[0][0]
    else: return None
  def id_to_word(self, *_ids): return [self._id_to_word(_id) for _id in _ids]
  def _word_to_id(self, word):
    res = self.cu.execute('SELECT id_word FROM words WHERE word=?', (word,)).fetchall()
    if res: return res[0][0]
    else: return None
  def word_to_id(self, *words): return [self._word_to_id(word) for word in words]

  # Работа с таблицей relations
  def get_max_id(self, name):
    return int(self.cu.execute('SELECT MAX(?) FROM relations', (name,)).fetchall[0][0])
  #def id_to_name()

  def _add_idwords_to_group(self, id_type, id_speech, id_group, isword, *id_words):
    ''' Добавляет id слов в существующую группу.
        Если id_group = None, то создастся новая группа'''
    if id_group==None: id_group = self.get_max_id('id_group') + 1
    for id_word in id_words:
      self.cu.execute('INSERT INTO relations (id_type, id_speech, id_group, id_word, isword) VALUES (?,?,?,?,?)',
                      (id_type, id_speech, id_group, id_word, isword))
    self.c.commit()
    return id_group
  def _get_idgroups_by_idword(self, isword, id_word, id_type=None, id_speech=None):
    ''' Возвращает id групп, в которых находится id слова '''
    if id_type != None and id_speech != None:
      res = self.cu.execute('SELECT id_group FROM relations WHERE id_type=?, id_speech=?, id_word=?, isword=?',
                      (id_type, id_speech, id_word, isword)).fetchall()
    elif id_type == None and id_speech != None:
      res = self.cu.execute('SELECT id_group FROM relations WHERE id_speech=?, id_word=?, isword=?',
                      (id_speech, id_word, isword)).fetchall()
    elif id_type != None and id_speech == None:
      res = self.cu.execute('SELECT id_group FROM relations WHERE id_type=?, id_word=?, isword=?',
                      (id_type, id_word, isword)).fetchall()
    else:
      res = self.cu.execute('SELECT id_group FROM relations WHERE id_word=?, isword=?',
                      (id_word, isword)).fetchall()
    return [_id[0] for _id in res] #FORAUTO id_groups
  def _get_idwords_by_idgroup(self, id_group, isword, id_type=None, id_speech=None):
    if id_type != None and id_speech != None:
      res1 = self.cu.execute('SELECT id_word FROM relations WHERE id_type=?, id_speech=?, id_group=?, isword=?',
                      (id_type, id_speech, id_group, isword)).fetchall()
    elif id_type == None and id_speech != None:
      res1 = self.cu.execute('SELECT id_word FROM relations WHERE id_speech=?, id_group=?, isword=?',
                      (id_speech, id_group, isword)).fetchall()
    elif id_type != None and id_speech == None:
      res1 = self.cu.execute('SELECT id_word FROM relations WHERE id_type=?, id_group=?, isword=?',
                      (id_type, id_group, isword)).fetchall()
    else:
      res1 = self.cu.execute('SELECT id_word FROM relations WHERE id_group=?, isword=?',
                      (id_group, isword)).fetchall()
    return [_id[0] for _id in res] #FORAUTO id_words

  # Составные функции для таблицы relations
  def _add_idwords_to_same_group(self, id_type, id_speech, isword, id_word, *id_words):
    ''' Добавляет все id_words в ту группу, в которой находится id_word.
        Если id_word не входит ни в одну группу, то оно добавится в новую группу'''
    id_groups = self._get_idgroups_by_idword(id_type, id_speech, isword, id_word)
    if id_groups == None:
      id_groups = [self._add_idwords_to_new_group(id_type, id_speech, isword, *id_words)]
    for id_group in id_groups:
      self._add_idwords_to_exist_group(id_type, id_speech, id_group, isword, *id_words)
  def _get_idwords_from_same_group(self, id_type, id_speech, isword, id_word):
    id_groups = self._get_idgroups_by_idword(id_type, id_speech, isword, id_word)
    id_words = []
    for id_group in id_groups:
      res = self._get_idwords_by_idgroup(self, id_group, isword, id_type, id_speech)
      if res: id_words += res
    return list(set(id_words)) #FORAUTO id_words
  def _is_idword_in_group(self, id_group, id_word, isword, id_type=None, id_speech=None):
    id_groups = self._get_idwords_by_idgroup(id_group, isword, id_type, id_speech)
    if id_word in id_groups: return True
    else: return False
  #def is_idwords_in_same_group(self, id_word1, isword1, id_word2, isword2, id_type=None, id_speech=None):
  '''def get_same_groups(self, id_word1, isword1, id_word2, isword2, id_type=None, id_speech=None):
    id_groups1 = get_idgroups_by_idword(isword1, id_word1, id_type, id_speech)
    id_groups2 = get_idgroups_by_idword(isword2, id_word2, id_type, id_speech)
    #id_common_groups = []
    #for id_group1 in id_groups1:
    #  if id_group1 in id_groups2: id_common_groups.append(id_group1)
    #return id_common_groups
    return [id_group1 for id_group1 in id_groups1 if id_group1 in id_groups2]'''
  def _get_same_groups(self, id_type, id_speech, *pairs):
    ''' Возвращает общие для всех id_word группы '''
    # pair = [id_word, isword]
    list_groups = []
    for pair in pairs:
      list_groups.append(self._get_idgroups_by_idword(pair[1], pair[0], id_type, id_speech))
    id_groups1 = list_groups.pop(0)
    matches = []
    for id_group in id_groups1:
      common_id_groups = []
      for id_groups in list_groups:
        if id_group in id_groups: matches.append(True)
      if len(common_id_groups) == len(list_groups): common_id_groups.append(id_group)
    id_groups2 = self._get_idgroups_by_idword(isword2, id_word2, id_type, id_speech)
    return common_id_groups #FORAUTO id_groups
