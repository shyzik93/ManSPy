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

  ### Работа с таблицей words

  def add_word(self, *words):
    for word in words:
      self.cu.execute('INSERT INTO words (word) VALUES (?)', (word.lower(),))
    self.c.commit()

  def convert(self, *inlist):
    ''' Преобразовывает id в слово или слово в id '''
    outlist = []
    for el in inlist:
      if isinstance(el, int): query = 'SELECT word FROM words WHERE id_word=?'
      else: query = 'SELECT id_word FROM words WHERE word=?'
      res = self.cu.execute(query, (el,)).fetchall()
      if res: outlist.append(res[0][0])
      else: outlist.append(None)
    return outlist

  ### Работа с таблицей relations (работают с идентификаторами)

  def get_max_id(self, name):
    return int(self.cu.execute('SELECT MAX(?) FROM relations', (name,)).fetchall[0][0])
  #def id_to_name()

  def _add_words2group(self, id_type, id_speech, id_group, isword, *id_words):
    ''' Добавляет слова в существующую группу.
        Если id_group = None, то создастся новая группа'''
    if id_group==None: id_group = self.get_max_id('id_group') + 1
    for id_word in id_words:
      self.cu.execute('INSERT INTO relations (id_type, id_speech, id_group, id_word, isword) VALUES (?,?,?,?,?)',
                      (id_type, id_speech, id_group, id_word, isword))
    self.c.commit()
    return id_group

  def _get_groups_by_word(self, isword, id_word, id_type=None, id_speech=None):
    ''' Возвращает группы, в которые входит слово '''
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

  def _get_words_by_group(self, id_group, isword, id_type=None, id_speech=None):
    ''' Возвращает слова, входящие в группу '''
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

  ### Составные функции для таблицы relations (работают с идентификаторами)

  def _add_words2samegroup(self, id_type, id_speech, isword, id_word, *id_words):
    ''' Добавляет все id_words в ту группу, в которой находится id_word.
        Если id_word не входит ни в одну группу, то оно добавится в новую группу'''
    id_groups = self._get_groups_by_word(id_type, id_speech, isword, id_word)
    if not id_groups:
      self._add_words2group(id_type, id_speech, None, isword, id_word)
      id_groups = self._get_groups_by_word(id_type, id_speech, isword, id_word)
    for id_group in id_groups:
      self._add_words2group(id_type, id_speech, id_group, isword, *id_words)

  def _get_words_from_samegroup(self, id_type, id_speech, isword, id_word):
    ''' Возвращает слова из той группы, в которую входит id_word '''
    id_groups = self._get_groups_by_word(id_type, id_speech, isword, id_word)
    id_words = []
    for id_group in id_groups:
      res = self._get_words_by_group(self, id_group, isword, id_type, id_speech)
      if res: id_words += res
    return list(set(id_words)) #FORAUTO id_words

  def _is_word_in_group(self, id_group, id_word, isword, id_type=None, id_speech=None):
    ''' Входит ли слово в группу? '''
    id_groups = self._get_words_by_group(id_group, isword, id_type, id_speech)
    #if id_word in id_groups: return True
    #else: return False
    return True if id_word in id_groups else False #FORAUTO True

  def _get_commongroups(self, id_type, id_speech, *pairs):
    ''' Возвращает общие для всех слов группы '''
    # pair = [id_word, isword]
    list_groups = []
    for pair in pairs:
      list_groups.append(self._get_groups_by_word(pair[1], pair[0], id_type, id_speech))

    common_id_groups = set(list_groups.pop(0))
    for list_group in list_groups:
      common_id_groups &= set(list_group)
    return list(common_id_groups) #FORAUTO id_groups

    #id_groups1 = list_groups.pop(0)
    #common_id_groups = []
    #for id_group in id_groups1:
    #  matches = []
    #  for id_groups in list_groups:
    #    if id_group in id_groups: matches.append(True)
    #  if len(matches) == len(list_groups): common_id_groups.append(id_group)
    #return common_id_groups #FORAUTO id_groups
