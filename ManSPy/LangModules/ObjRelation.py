# -*- coding: utf-8 -*-
import sqlite3 as sql, os, pickle
import Relation_new

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

def max_create(cu, c, name_table='None'):
  name_table = 'max_' + name_table
  cu.execute("CREATE TABLE IF NOT EXISTS %s (max_id INTEGER);" % name_table) # максимальный ID группы + 1
  # проверяем наличие записи. Если она уже есть, то добавляять её тогда не следует.
  res = cu.execute("SELECT max_id FROM %s;" % name_table)
  if res.fetchall(): return

  cu.execute("INSERT INTO %s (max_id) VALUES (?);" % name_table, (0,))
  c.commit()

def max_increment(cu, c, name_table):
  name_table = 'max_' + name_table
  max_id = cu.execute(" SELECT max_id FROM %s; " % name_table).fetchall()[0][0]
  max_id += 1
  cu.execute(" UPDATE %s SET max_id=?;" % name_table, (max_id,))
  c.commit()
  return max_id-1

class SynonymsDB():
  """ База синонимов """
  c = cu = None
  exist_tables = ['verb', 'noun', 'adverb', 'adjective']
  def __init__(self, language):
    self.c, self.cu = create_bd_file(language, 'synonym.db')
    for name_table in self.exist_tables:
      self.cu.execute("""
        CREATE TABLE IF NOT EXISTS %s (
          id_word INTEGER UNIQUE ON CONFLICT IGNORE,
          id_group INTEGER,
          date TEXT DEFAULT CURRENT_TIMESTAMP
        );""" % name_table) # ID слова; ID группы синонимов; Дата добавления
      max_create(self.cu, self.c, name_table)

  def add(self, POSpeech, id_word, id_group=None, type_id="group"):
    """ Добавляет новый глагол. Если указана id_group, то глагол добавляется к
        существующей группе, иначе - создаётся новая группа синонимов и
        возвращаеттся её индекс.
        Также если в id_group передадим id глагола, а не группы,
        и укажем type_id как "verb", то id глагола добавиться в группу,
        в которой находится id второго глагола."""
    if id_group == None:
      res = self.cu.execute("SELECT id_group FROM %s WHERE id_word=?" % POSpeech, (id_word,)).fetchall()
      #print "#"*10, "\n", res
      if len(res) == 1: return res[0][0] # если глагол уже есть, то вернём его группу
      #print POSpeech
      id_group = max_increment(self.cu, self.c, POSpeech)
    if type_id == "word":
      id_group = self.cu.execute(" SELECT id_group FROM %s WHERE id_word=?;" % POSpeech, (id_word,)).fetchall()[0][0]
    self.cu.execute("INSERT INTO %s (id_word, id_group) VALUES (?, ?); " % POSpeech, (id_word, id_group))
    self.c.commit()
    return id_group

  def get_id_group(self, POSpeech, id_word):
    res = self.cu.execute("SELECT id_group FROM %s WHERE id_word=?" % POSpeech, (id_word,)).fetchall()
    if res: return res[0][0]

  def get_id_word(self, POSpeech, id_group):
    res = self.cu.execute("SELECT id_word FROM %s WHERE id_group=?" % POSpeech, (id_group,)).fetchall()
    if res: return res[0][0]

  def get_synonyms(self, POSpeech, id_word, type_id="group"):
    if type_id == "word":
      id_group = self.cu.execute("SELECT id_group FROM %s WHERE id_word=?;" % POSpeech, (id_group,)).fetchall()[0][0]
    return self.cu.execute("SELECT id_word FROM %s WHERE id_group=?;" % POSpeech, (id_word,)).fetchall()[0]

  def close(self):
    self.cu.close()
    self.c.close()

class AntonymsDB:
  c = cu = None
  base = ['noun', 'adjective', 'adverb']
  exist_tables = ['verb', 'base'] # verb - для глаголов, base - для существительных, прилагательных и наречий.
  def __init__(self, language):
    self.c, self.cu = create_bd_file(language, 'antonym.db')
    for name_table in self.exist_tables:
      self.cu.execute("""
        CREATE TABLE IF NOT EXISTS %s (
          id_synonym_group1 INTEGER UNIQUE ON CONFLICT IGNORE,
          id_synonym_group2 INTEGER UNIQUE ON CONFLICT IGNORE,
          date TEXT DEFAULT CURRENT_TIMESTAMP
        );
      """ % name_table) # ID группы синонимов; ID противоположной группы синонимов; дата
      max_create(self.cu, self.c, name_table)

  def add(self, POSPeech, id_synonym_group1, id_synonym_group2):
    if POSpeech in self.base: POSpeech = 'base'
    self.cu.execute(""" INSERT INTO %s (id_synonym_group1, id_synonym_group2) VALUES (?, ?) """ % POSpeech,
                    (id_synonym_group1, id_synonym_group2))

  def get(self, POSpeech, id_synonym_group1):
    if POSpeech in self.base: POSpeech = 'base'
    res = self.cu.execute(""" SELECT id_synonym_group1, id_synonym_group2 FROM %s WHERE (id_synonym_group1=? OR id_synonym_group2=?)""" % POSpeech,
                    (id_synonym_group1, id_synonym_group1)).fetchall()
    if not res: return
    _id1, _id2 = res[0]
    if id_synonym_group1 != _id1: return _id1
    else: return _id2

class ListOfWordsDB:
  """ Список слов с порядковыми номерами, так как оперировать легче номерами,
      чем многобайтовыми строками.
  """
  c = cu = None
  def __init__(self, language):
    self.c, self.cu = create_bd_file(language, "list_words.db")
    self.cu.execute("""
      CREATE TABLE IF NOT EXISTS words (
        word TEXT COLLATE NOCASE UNIQUE ON CONFLICT IGNORE,
        id INTEGER PRIMARY KEY,
        date TEXT DEFAULT CURRENT_TIMESTAMP
      );
    """) # Слово; ID слова; Дата добавления

  def add(self, word):
    self.cu.execute("INSERT INTO words (word) VALUES (?);", (word,))
    self.c.commit()
    # эту строку необходимо реализовать через таблицу с максимальным id.
    # Это увеличит скорость, так как в некоторых случаях необходимо получить id
    # сразу после добавления.
    #return self.selectIndex(word)

  def selectWord(self, word_id):
    res = self.cu.execute("SELECT word FROM words WHERE id=?;", (word_id,)).fetchall()
    if res: return res[0][0]
    else: return None
  
  def selectId(self, word):
    ''' Возвращает слово по id. Если слово не в базе, то оно добавиться. '''
    res = self.cu.execute("SELECT id FROM words WHERE word=?;", (word,))
    res = res.fetchall()
    if len(res) == 0:
      self.add(word)
      return self.selectId(word)
    return res[0][0]

  def close(self):
    self.cu.close()
    self.c.close()

  def addFromList(self, list_words, close=0):
    for word in list_words:
      self.add(word)
    if close: self.close()

class AbstractGroupsDB():
  """ База абстрактных групп существительных """
  def __init__(self, language):
    self.c, self.cu = create_bd_file(language, "abstract_groups.db")
    self.cu.execute("""CREATE TABLE IF NOT EXISTS groups (
      id_group INTEGER,
      id INTEGER,
      type_id TEXT,
      date TEXT DEFAULT CURRENT_TIMESTAMP
    );""")

  def addGroup(self, id_group, id_, type_id='word'):
    """ type_id позволяет добавлять в группу не только слова, но и группы. """
    res = self.cu.execute("SELECT date FROM groups WHERE id_group=? AND id=? AND type_id=?", (id_group, id_, type_id))
    if len(res.fetchall()) == 0:
      self.cu.execute("INSERT INTO groups (id_group, id, type_id) VALUES (?,?,?)", (id_group, id_, type_id))
      self.c.commit()

  def getWordsInGroup(self, id_group): # какие слова входят в указанную группу
    res = self.cu.execute("SELECT id FROM groups WHERE type_id='word' AND id_group=?", (id_group, ))
    res = res.fetchall()
    res = [i[0] for i in res]
    return res

class ProcFASIF():
  """ База хранимых ФАСИФов """
  def __init__(self, language, test=0):
    self.test = test
    self.c, self.cu = create_bd_file(language, "procFASIF.db")
    self.cu.execute("""
      CREATE TABLE IF NOT EXISTS procFASIF (
        id_group_verb INTEGER,
        id_group_noun INTEGER,
        function_data TEXT,
        date TEXT DEFAULT CURRENT_TIMESTAMP
      );""") # ID группы синонимии глаголов; ID абстрактной группы существительных; Хранимый ФАСИФ; Дата добавления
    # вместо ID абстрактной группы добавляется ID слова.

  def add(self, id_verb_group, id_noun, function_data):
    # проверяем наличие записи. Если она уже есть, то добавляять её тогда не следует.
    res = self.cu.execute(""" SELECT function_data FROM procFASIF WHERE id_group_verb=? AND id_group_noun=?;""", (id_verb_group, id_noun))
    if res.fetchall(): return
    if self.test: function_data = str(function_data)
    else: function_data = pickle.dumps(function_data)
    self.cu.execute(""" INSERT INTO procFASIF (id_group_verb, id_group_noun, function_data) VALUES (?,?,?)""", (id_verb_group, id_noun, function_data))
    self.c.commit()

  def get(self, id_verb_group, id_noun):
    #print 'get FASIF', id_verb_group, id_noun
    res = self.cu.execute(" SELECT function_data FROM procFASIF WHERE id_group_verb=? AND id_group_noun=?;", (id_verb_group, id_noun))
    res = res.fetchall()
    if not res: return
    if self.test: return eval(res[0][0])
    else: return pickle.loads(res[0][0])

  def update(self, id_group_verb, id_group, function_data):
    self.cu.execute("UPDATE procFACIF SET function_data=? WHERE id_group_verb=? AND id_group_noun=?;", (function_data, id_group_verb, id_group))
    self.c.commit()

class ObjRelation():
  """ Надкласс, реализующий высокий уровень работы с разными группами слов, абстрагируясь от БД.
      Другими словами, он задествует вышеуказанные классы для реализации своих
      функций."""
  def __init__(self, language, test=0, version=1):
    self.version = version
    if version == 1:
      self.LOWDB = ListOfWordsDB(language)
      self.AGDB = AbstractGroupsDB(language)
      self.SDB = SynonymsDB(language)
      self.ADB = AntonymsDB(language)
      self.PFASIF = ProcFASIF(language, test)
    elif version == 2: self.R = Relation_new.Relation(language, test)

  # к удалению во второй версии базы
  def _ids2words(self, list_ids):
    return [self.LOWDB.selectWord(word_id) for word_id in list_ids]

  # Сделано!
  def isWordInAbstractGroup(self, word_base, group_base):
    if self.version == 1:
      word_id = self.LOWDB.selectId(word_base)
      group_id = self.LOWDB.selectId(group_base)
      words_in_group = self.AGDB.getWordsInGroup(group_id)
      if word_id in words_in_group: return True
      else: return False
    elif self.version == 2:
      #print 'isWordInAbstractGroup', group_base, word_base
      return self.R.is_word_in_group('abstract', group_base, word_base, 0, None)

  # Сделано! Составная
  def areWordsAntonyms(self, POSpeech, word_base1, word_base2):
    if self.version == 1:
      word_id1 = self.LOWDB.selectId(word_base1)
      word_id2 = self.LOWDB.selectId(word_base2)
      id_synonym_group1 = self.SDB.get_id_group(POSpeech, word_id1)
      id_synonym_group2 = self.ADB.get(POSpeech, id_synonym_group1)
      synonym_group2 = self.SDB.get_synonyms(POSpeech, id_synonym_group2)
      if word_id2 in synonym_group2: return True
      else: return False
    elif self.version == 2:
      antonyms = self.getAntonyms(POSpeech, word_base1)
      if word_base2 in antonyms: return True
      else: False

  # Сделано!
  def getAntonyms(self, POSpeech, word_base):
    if self.version == 1:
      word_id = self.LOWDB.selectId(word_base)
      id_synonym_group = self.SDB.get_id_group(POSpeech, word_id)
      id_synonym_group = self.ADB.get(POSpeech, id_synonym_group) # группа синонимов, являющихся анитонимаии относительно предыдущей группы синонимов
      if not id_synonym_group: return []
      list_ids = self.SDB.get_synonyms(POSpeech, id_synonym_group)
      return self._ids2words(list_ids)
    elif self.version == 2:
      '''#is_word_in_group(self, id_group, word, isword, id_type=None, id_speech=None):
      id_group = word_base # так как это антоним. Проверка должна происходить в ниженаписанной функции
      self.R.get_words_by_group(id_group, isword, 'antonym', POSpeech)
      #return self.R.get_commongroups('synonym', POSpeech, [word_base, 0])'''
      syn_groups = self.R.get_groups_by_word('synonym', 0, word_base, POSpeech)
      if not syn_groups: return []
      syn_groups = self.R.get_words_from_samegroup('antonym', POSpeech, self.R.dct_types['synonym'], syn_groups[0])
      if not syn_groups: return []
      return self.R.convert(self.R.get_words_by_group('synonym', syn_group, 0, POSpeech))

  # Сделано!
  def getSynonyms(self, POSpeech, word_base):
    if self.version == 1:
      word_id = self.LOWDB.selectId(word_base)
      list_ids = self.SDB.get_synonyms(POSpeech, word_id)
      if not list_ids: return []
      return self._ids2words(list_ids)
    elif self.version == 2:
      return self.R.convert(self.R.get_words_from_samegroup('synonym', POSpeech, 0, word_base))

  def get(self, relation, POSpeech, word_base):
    if relation == 'antonyms': return self.getAntonyms(POSpeech, word_base)
    elif relation == 'synonyms': return self.getSynonyms(POSpeech, word_base)

  def procFASIF(self, verb_base, noun_base, procFASIF=None):
    if self.version == 1:
      noun_id = self.LOWDB.selectId(noun_base)
      verb_id = self.LOWDB.selectId(verb_base)
      verb_synonym_group_id = self.SDB.get_id_group('verb', verb_id)

      if procFASIF: self.PFASIF.add(verb_synonym_group_id, noun_id, procFASIF)
      else:
        isantonym = False
        procFASIF = self.PFASIF.get(verb_synonym_group_id, noun_id)
        if not procFASIF:
          #  если ФАСИФ не найден, то пробуем извлечь по антониму
          verb_synonym_group_id = self.ADB.get('verb', verb_synonym_group_id)
          print 'verb_synonym_group_id (antonym)', verb_synonym_group_id
          procFASIF = self.PFASIF.get(verb_synonym_group_id, noun_id)
          isantonym = True
        return procFASIF, isantonym
    elif self.version == 2:
      return self.R.procFASIF(verb_base, noun_base, procFASIF)

  def addWordsToDBFromDictSentence(self, dict_sentence):
    if "dict" in str(type(dict_sentence)): indexes = dict_sentence.keys()
    elif "list" in str(type(dict_sentence)): indexes = range(len(dict_sentence))
    for index in indexes:
      dword = dict_sentence[index]
      # числительные в базу не добавляем
      #if dict_sentence[index]['POSpeech'] == 'number': continue
      if self.version == 1: word_id = self.LOWDB.selectId(dword['base'])
      elif self.version == 2:
        self.R.add_word(dword['base'])
        #word_id = self.R.convert(dword['base'])
      if len(dword['feature']) != 0: self.addWordsToDBFromDictSentence(dword['feature'])
      if dword['MOSentence'] == 'predicate' and dword['POSpeech'] == 'verb':
        if self.version == 1: id_synonym_group = self.SDB.add(dword['POSpeech'], word_id)
        elif self.version == 2: self.R.add_words2group('synonym', dword['POSpeech'], None, 0, dword['base'])

  def addWordsInAbstractGroup(self, group_base, *word_bases):
    ''' Добавляем абстрактные группы. Новые слова также добавляются в базу слов. '''
    if self.version == 1:
      group_id = self.LOWDB.selectId(group_base)
      for word_base in word_bases:
        if not word_base: continue
        word_id = self.LOWDB.selectId(word_base)
        self.AGDB.addGroup(group_id, word_id)
    elif self.version == 2:
      print group_base, word_bases
      self.R.add_words2group('abstract', None, group_base, 0, *word_bases)

def toShowDB():
  lang = 'Esperanto'
  #LOWDB = ListOfWordsDB(lang)
  #ADB = AntonymsDB(lang)
  #SDB = SynonymsDB(lang)
  #AGDB = AbstractGroupsDB(lang)
  #PFASIF = ProcFASIF(lang, 1)
  OR = ObjRelation(lang, 1)
  print '\n', '--' * 10, 'Abstract groups'
  res = OR.AGDB.cu.execute('SELECT MAX(id_group) FROM groups WHERE type_id="word"').fetchall()[0][0]
  if not res: res= 0
  for id_group in range(res):
    words = OR.AGDB.getWordsInGroup(id_group)
    if words: print OR.LOWDB.selectWord(id_group), OR._ids2words(words)

  print '\n', '--' * 10, 'FASIFs'
  res = OR.PFASIF.cu.execute('SELECT id_group_verb, id_group_noun FROM procFASIF').fetchall()
  if not res: res = []
  for words in res:
    print words, OR._ids2words(words)

#toShowDB()
