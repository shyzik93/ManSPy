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
    # Можно подавать как слова, так и списки слов
    for word in words:
      if isinstance(word, list): self.add_word(*word)
      else: self.cu.execute('INSERT INTO words (word) VALUES (?);', (word.lower(),))
    self.c.commit()

  def convert(self, *inlist):
    ''' Преобразовывает id в слово или слово в id '''
    outlist = []
    for el in inlist:
      if isinstance(el, int): query = 'SELECT word FROM words WHERE id_word=?;'
      else: query = 'SELECT id_word FROM words WHERE word=?;'
      res = self.cu.execute(query, (el,)).fetchall()
      if res: outlist.append(res[0][0])
      else: outlist.append(None)
    return outlist

  ### Работа с таблицей relations (работают с идентификаторами)

  def get_max_id(self, name, id_type=None):
    if id_type == None: res = self.cu.execute('SELECT MAX(%s) FROM relations;'%name).fetchall()[0][0]
    else: res = self.cu.execute('SELECT MAX(%s) FROM relations WHERE id_type=?;'%name, (id_type, )).fetchall()[0][0]
    return res if res != None else 0
  #def id_to_name()

  def _add_words2group(self, id_type, id_speech, id_group, isword, *id_words):
    ''' Добавляет слова в существующую группу.
        Если id_group = None, то создастся новая группа'''
    if id_group==None: id_group = self.get_max_id('id_group', id_type) + 1
    for id_word in id_words:
      self.cu.execute('INSERT INTO relations (id_type, id_speech, id_group, id_word, isword) VALUES (?,?,?,?,?);',
                      (id_type, id_speech, id_group, id_word, isword))
    self.c.commit()
    return id_group

  def _get_groups_by_word(self, isword, id_word, id_type, id_speech=None):
    ''' Возвращает группы, в которые входит слово '''
    if id_speech != None:
      res = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_speech=? AND id_word=? AND isword=?',
                      (id_type, id_speech, id_word, isword)).fetchall()
    else:
      res = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_word=? AND isword=?',
                      (id_type, id_word, isword)).fetchall()
    return [_id[0] for _id in res] #FORAUTO id_groups

  def _get_words_by_group(self, id_group, isword, id_type, id_speech=None):
    ''' Возвращает слова, входящие в группу '''
    if id_speech != None:
      res = self.cu.execute('SELECT id_word FROM relations WHERE id_type=? AND id_speech=? AND id_group=? AND isword=?;',
                      (id_type, id_speech, id_group, isword)).fetchall()
    else:
      res = self.cu.execute('SELECT id_word FROM relations WHERE id_type=? AND id_group=? AND isword=?',
                      (id_type, id_group, isword)).fetchall()
    return [_id[0] for _id in res] #FORAUTO id_words

  ### Составные функции для таблицы relations (работают с идентификаторами)

  def _add_words2samegroup(self, id_type, id_speech, isword, id_word, *id_words):
    ''' Добавляет все id_words в ту группу, в которой находится id_word.
        Если id_word не входит ни в одну группу, то оно добавится в новую группу'''
    id_groups = self._get_groups_by_word(isword, id_word, id_type, id_speech)
    #id_groups = self._get_groups_by_word(id_type, id_speech, isword, id_word)
    if not id_groups:
      self._add_words2group(id_type, id_speech, None, isword, id_word)
      id_groups = self._get_groups_by_word(id_type, id_speech, isword, id_word)
    for id_group in id_groups:
      self._add_words2group(id_type, id_speech, id_group, isword, *id_words)

  def _get_words_from_samegroup(self, id_type, id_speech, isword, id_word):
    ''' Возвращает слова из той группы, в которую входит id_word ''' #работает медленно
    id_groups = self._get_groups_by_word(isword, id_word, id_type, id_speech)
    #id_groups = self._get_groups_by_word(id_type, id_speech, isword, id_word)
    id_words = []
    for id_group in id_groups:
      res = self._get_words_by_group(id_group, isword, id_type, id_speech)
      if res: id_words.extend(res)
    return list(set(id_words)) #FORAUTO id_words

  def _is_word_in_group(self, id_group, id_word, isword, id_type, id_speech=None):
    ''' Входит ли слово в группу? '''
    id_groups = self._get_words_by_group(id_group, isword, id_type, id_speech)
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

if __name__ == '__main__':
  R = _Relation('Esperanto')
  list_words = ['dom', 'kot', 'kosxar', 'aparat', 'montr', 'sobak', 'peos']
  R.add_word(list_words)
  print u"Добавили слова в базу. Их id:", R.convert(*list_words)

  lst = R.convert('kot', 'kosxar')
  id_group = R._add_words2group(1, 'noun', None, 0, *lst)
  print u"Добавили слова в группу:", lst, id_group

  lst = R.convert('sobak', 'peos')
  id_group = R._add_words2group(1, 'noun', None, 0, *lst)
  print u"Добавили слова в группу:", lst, id_group

  id_word = lst[0]
  R._add_words2samegroup(1, 'noun', 0, id_word, *R.convert('aparat'))
  print u"Все слова в группе с %i" % id_word, R._get_words_from_samegroup(1, 'noun', 0, id_word)
  print u"Все слова в группе %i" % id_group, R._get_words_by_group(id_group, 0, 1, 'noun')
  print u"Все группы, куда входит слово %i" % id_word, R._get_groups_by_word(0, id_word, 1, 'noun')
  print u"Слово %i в группе %i?" % (id_word, id_group), R._is_word_in_group(id_group, id_word, 0, 1, 'noun')
  print R._get_commongroups(1, 'noun', [id_word, 0], [lst[1],0], [R.convert('aparat')[0], 0])
