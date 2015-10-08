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

class Relation():
  dct_types = {'synonym': 1, 'antonym': 2, 'abstract': 3}
  dct_speeches = {'noun': 1, 'verb': 2, 'adjective': 3, 'adverb': 4}
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
    ''' Можно подавать как слова, так и списки слов '''
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

  def _word2id(self, word):
    if isinstance(word, str) or isinstance(word, unicode):
      return self.cu.execute('SELECT id_word FROM words WHERE word=?;', (word,)).fetchall()[0][0]
    else: return word
  def _type2id(self, _type): return self.dct_types[_type] if isinstance(_type, str) or isinstance(_type, unicode) else _type
  def _speech2id(self, speech): return self.dct_speeches[speech] if isinstance(speech, str) or isinstance(speech, unicode) else speech

  ### Работа с таблицей relations

  def get_max_id(self, name, id_type=None):
    if id_type == None: res = self.cu.execute('SELECT MAX(%s) FROM relations;'%name).fetchall()[0][0]
    else: res = self.cu.execute('SELECT MAX(%s) FROM relations WHERE id_type=?;'%name, (id_type, )).fetchall()[0][0]
    return res if res != None else 0

  def add_words2group(self, id_type, id_speech, id_group, isword, *id_words):
    ''' Добавляет слова в существующую группу.
        Если id_group = None, то создастся новая группа'''
    if id_group==None: id_group = self.get_max_id('id_group', self._type2id(id_type)) + 1
    for id_word in id_words:
      self.cu.execute('INSERT INTO relations (id_type, id_speech, id_group, id_word, isword) VALUES (?,?,?,?,?);',
                      (self._type2id(id_type), self._speech2id(id_speech), self._word2id(id_group), self._word2id(id_word), self._type2id(isword)))
    self.c.commit()
    return id_group

  def get_groups_by_word(self, id_type, isword, id_word, id_speech=None):
    ''' Возвращает группы, в которые входит слово '''
    if id_speech != None:
      res = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_speech=? AND id_word=? AND isword=?',
                      (self._type2id(id_type), self._speech2id(id_speech), self._word2id(id_word), self._type2id(isword))).fetchall()
    else:
      res = self.cu.execute('SELECT id_group FROM relations WHERE id_type=? AND id_word=? AND isword=?',
                      (self._type2id(id_type), self._word2id(id_word), self._type2id(isword))).fetchall()
    return [_id[0] for _id in res]

  def get_words_by_group(self, id_type, id_group, isword, id_speech=None):
    ''' Возвращает слова, входящие в группу '''
    if id_speech != None:
      res = self.cu.execute('SELECT id_word FROM relations WHERE id_type=? AND id_speech=? AND id_group=? AND isword=?;',
                      (self._type2id(id_type), self._speech2id(id_speech), id_group, self._type2id(isword))).fetchall()
    else:
      res = self.cu.execute('SELECT id_word FROM relations WHERE id_type=? AND id_group=? AND isword=?',
                      (self._type2id(id_type), id_group, self._type2id(isword))).fetchall()
    return [_id[0] for _id in res]

  ### Составные функции для таблицы relations (работают с идентификаторами)

  def add_words2samegroup(self, id_type, id_speech, isword, id_word, *id_words):
    ''' Добавляет все id_words в ту группу, в которой находится id_word.
        Если id_word не входит ни в одну группу, то оно добавится в новую группу'''
    id_groups = self.get_groups_by_word(id_type, isword, id_word, id_speech)
    #id_groups = self.get_groups_by_word(id_type, id_speech, isword, id_word)
    if not id_groups:
      self.add_words2group(id_type, id_speech, None, isword, id_word)
      id_groups = self.get_groups_by_word(id_type, id_speech, isword, id_word)
    for id_group in id_groups:
      self.add_words2group(id_type, id_speech, id_group, isword, *id_words)

  def get_words_from_samegroup(self, id_type, id_speech, isword, id_word):
    ''' Возвращает слова из той группы, в которую входит id_word ''' #работает медленно
    id_groups = self.get_groups_by_word(id_type, isword, id_word, id_speech)
    id_words = []
    for id_group in id_groups:
      res = self.get_words_by_group(id_type, id_group, isword, id_speech)
      if res: id_words.extend(res)
    return list(set(id_words))

  def is_word_in_group(self, id_type, id_group, id_word, isword, id_speech=None):
    ''' Входит ли слово в группу? '''
    id_words = self.get_words_by_group(id_type, id_group, isword, id_speech)
    return True if self._word2id(word) in id_words else False

  def get_commongroups(self, id_type, id_speech, *pairs):
    ''' Возвращает общие для всех слов группы '''
    # pair = [id_word, isword]
    list_groups = []
    for pair in pairs:
      list_groups.append(self.get_groups_by_word(id_type, pair[1], pair[0], id_speech))

    common_id_groups = set(list_groups.pop(0))
    for list_group in list_groups:
      common_id_groups &= set(list_group)
    return list(common_id_groups)

if __name__ == '__main__':
  R = Relation('Esperanto')
  list_words = ['dom', 'kot', 'kosxar', 'aparat', 'montr', 'sobak', 'peos']
  R.add_word(list_words)
  print u"Добавили слова в базу. Их id:", R.convert(*list_words)

  lst = ['kot', 'kosxar']
  id_group = R.add_words2group('synonym', 'noun', None, 0, *lst)
  print u"Добавили слова в группу:", lst, id_group

  lst = ['sobak', 'peos']
  id_group = R.add_words2group('synonym', 'noun', None, 0, *lst)
  print u"Добавили слова в группу:", lst, id_group

  word = 'sobak'
  R.add_words2samegroup('synonym', 'noun', 0, word, 'aparat')
  print u"Все слова в группе с %s" % word, R.convert(*R.get_words_from_samegroup('synonym', 'noun', 0, word))
  print u"Все слова в группе %s" % id_group, R.convert(*R.get_words_by_group('synonym', id_group, 0, 'noun'))
  print u"Все группы, куда входит слово %s:" % word, R.get_groups_by_word('synonym', 0, word, 'noun')
  print u"Слово %s в группе %s?" % (word, id_group), R.is_word_in_group('synonym', id_group, word, 0, 'noun')
  print R.get_commongroups('synonym', 'noun', [word, 0], [lst[1],0], [R.convert('aparat')[0], 0])
