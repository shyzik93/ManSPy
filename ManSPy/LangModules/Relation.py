# -*- coding: utf-8 -*-
#import sqlite3 as sql, os
import pickle
from ManSPy import GeneralForDB

class Relation():
  dct_types = {'synonym': 1, 'antonym': 2, 'abstract': 3}
  dct_speeches = {'noun': 1, 'verb': 2, 'adjective': 3, 'adverb': 4}
  
  def __init__(self, language, test=0):
    self.test = test
    self.c, self.cu = GeneralForDB.create_bd_file(language, 'main_data.db')
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
      CREATE TABLE IF NOT EXISTS procFASIF (
        id_group_verb INTEGER,
        id_group_noun INTEGER,
        function_data TEXT,
        date TEXT DEFAULT CURRENT_TIMESTAMP);''')
    self.dct_typesR = {}
    for k, v in self.dct_types.items(): self.dct_typesR[v] = k
    self.dct_speechesR = {}
    for k, v in self.dct_speeches.items(): self.dct_speechesR[v] = k

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
      else: # если слово отсутствует, то добавим его
        self.add_word(el)
        outlist.append(*convert(el))
    return outlist

  def _word2id(self, word):
    if isinstance(word, str) or isinstance(word, unicode):
      res = self.cu.execute('SELECT id_word FROM words WHERE word=?;', (word,)).fetchall()
      if res: return res[0][0]
      else: # если слово отсутствует, то добавим его
        self.add_word(word) 
        return self._word2id(word)
    else: return word
  def _type2id(self, _type): return self.dct_types[_type] if isinstance(_type, str) or isinstance(_type, unicode) else _type
  def _speech2id(self, speech): return self.dct_speeches[speech] if isinstance(speech, str) or isinstance(speech, unicode) else speech

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

  def add_words2group(self, id_type, id_speech, id_group, isword, *id_words):
    ''' Добавляет слова в существующую группу.
        Если id_group = None, то создастся новая группа'''
    id_groups = []
    _exists = id_group
    if id_group==None: id_group = self.get_max_id('id_group', self._type2id(id_type)) + 1
    for id_word in id_words:
      _id_group = self.check_copy_row(id_type, id_speech, id_group, id_word, isword, _exists)
      print _id_group
      if _id_group == False:
        self.cu.execute('INSERT INTO relations (id_type, id_speech, id_group, id_word, isword) VALUES (?,?,?,?,?);',
                      (self._type2id(id_type), self._speech2id(id_speech), self._word2id(id_group), self._word2id(id_word), self._type2id(isword)))
        id_groups.append(id_group)
      else: id_groups.append(_id_group)
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
                      (self._type2id(id_type), self._speech2id(id_speech), self._word2id(id_group), self._type2id(isword))).fetchall()
    else:
      res = self.cu.execute('SELECT id_word FROM relations WHERE id_type=? AND id_group=? AND isword=?',
                      (self._type2id(id_type), self._word2id(id_group), self._type2id(isword))).fetchall()
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
    return self._word2id(id_word) in id_words

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

  # Работа с таблицей procFASIF

  def _add_pFASIF(self, id_verb_group, id_noun, function_data):
    # проверяем наличие записи. Если она уже есть, то добавляять её тогда не следует.
    res = self.cu.execute("SELECT function_data FROM procFASIF WHERE id_group_verb=? AND id_group_noun=?;",
                          (id_verb_group, self._word2id(id_noun)))
    if res.fetchall(): return
    function_data = str(function_data) if self.test else pickle.dumps(function_data)
    self.cu.execute("INSERT INTO procFASIF (id_group_verb, id_group_noun, function_data) VALUES (?,?,?)",
                    (id_verb_group, self._word2id(id_noun), function_data))
    self.c.commit()

  def _get_pFASIF(self, id_verb_group, id_noun):
    #print 'get FASIF', id_verb_group, id_noun
    res = self.cu.execute(" SELECT function_data FROM procFASIF WHERE id_group_verb=? AND id_group_noun=?;",
                          (id_verb_group, self._word2id(id_noun)))
    res = res.fetchall()
    if not res: return
    return eval(res[0][0]) if self.test else pickle.loads(res[0][0])

  def _update_pFASIF(self, id_group_verb, id_noun, function_data):
    self.cu.execute("UPDATE procFACIF SET function_data=? WHERE id_group_verb=? AND id_group_noun=?;", (function_data, id_group_verb, self._word2id(id_noun)))
    self.c.commit()

  def procFASIF(self, id_verb, id_noun, procFASIF=None, update=None):
    ''' Извлечение, добавление, обновление хранимого ФАСИФа. '''
    verb_synonym_group_id = self.get_groups_by_word('synonym', 0, id_verb, 'verb')[0] # подумать

    if procFASIF:
      self._add_pFASIF(verb_synonym_group_id, id_noun, procFASIF)
      return
    elif update:
      self._update_pFASIF(verb_synonym_group_id, id_noun, function_data)
      return

    isantonym = False
    procFASIF = self._get_pFASIF(verb_synonym_group_id, id_noun)
    if not procFASIF:
      #  если ФАСИФ не найден, то пробуем извлечь по антониму
      verb_synonym_group_id = self._get_words_from_samegroup('antonym', 'verb', 'synonym', verb_synonym_group_id)
      #print 'verb_synonym_group_id (antonym)', verb_synonym_group_id
      procFASIF = self._get_pFASIF(verb_synonym_group_id, id_noun)
      if not procFASIF: return None, isantonym
      isantonym = True
    return procFASIF, isantonym

class _ObjRelation(object):
  """ Надкласс, реализующий высокий уровень работы с разными группами слов, абстрагируясь от БД.
      Другими словами, он задествует вышеуказанные классы для реализации своих
      функций."""
  def __init__(self, language, test=0):
    self.R = Relation(language, test)

  def isWordInAbstractGroup(self, word_base, group_base):
    #print 'isWordInAbstractGroup', group_base, word_base
    return self.R.is_word_in_group('abstract', group_base, word_base, 0, None)

  def areWordsAntonyms(self, POSpeech, word_base1, word_base2):
    antonyms = self.getAntonyms(POSpeech, word_base1)
    return word_base2 in antonyms

  def getAntonyms(self, POSpeech, word_base):
    '''#is_word_in_group(self, id_group, word, isword, id_type=None, id_speech=None):
    id_group = word_base # так как это антоним. Проверка должна происходить в ниженаписанной функции
    self.R.get_words_by_group(id_group, isword, 'antonym', POSpeech)
    #return self.R.get_commongroups('synonym', POSpeech, [word_base, 0])'''
    syn_groups = self.R.get_groups_by_word('synonym', 0, word_base, POSpeech)
    if not syn_groups: return []
    syn_groups = self.R.get_words_from_samegroup('antonym', POSpeech, self.R.dct_types['synonym'], syn_groups[0])
    if not syn_groups: return []
    return self.R.convert(self.R.get_words_by_group('synonym', syn_group, 0, POSpeech))

  def getSynonyms(self, POSpeech, word_base):
    return self.R.convert(self.R.get_words_from_samegroup('synonym', POSpeech, 0, word_base))

  def get(self, relation, POSpeech, word_base):
    if relation == 'antonyms': return self.getAntonyms(POSpeech, word_base)
    elif relation == 'synonyms': return self.getSynonyms(POSpeech, word_base)

  def procFASIF(self, verb_base, noun_base, procFASIF=None):
    return self.R.procFASIF(verb_base, noun_base, procFASIF)

  def addWordsToDBFromDictSentence(self, dict_sentence):
    if "dict" in str(type(dict_sentence)): indexes = dict_sentence.keys()
    elif "list" in str(type(dict_sentence)): indexes = range(len(dict_sentence))
    for index in indexes:
      dword = dict_sentence[index]
      # числительные в базу не добавляем
      #if dict_sentence[index]['POSpeech'] == 'number': continue
      self.R.add_word(dword['base'])
      #word_id = self.R.convert(dword['base'])
      if len(dword['feature']) != 0: self.addWordsToDBFromDictSentence(dword['feature'])
      if dword['MOSentence'] == 'predicate' and dword['POSpeech'] == 'verb':
        self.R.add_words2group('synonym', dword['POSpeech'], None, 0, dword['base'])

  def addWordsInAbstractGroup(self, group_base, *word_bases):
    ''' Добавляем абстрактные группы. Новые слова также добавляются в базу слов. '''
    print group_base, word_bases
    self.R.add_words2group('abstract', None, group_base, 0, *word_bases)

if __name__ == '__main__':
  R = Relation('Esperanto')

  rng = range(1, R.get_max_id('id_type')+1)
  for id_type in rng:
    print R.dct_typesR[id_type]
    res = R.cu.execute('SELECT id_group, id_word, isword FROM relations WHERE id_type=? ORDER BY id_group;', (id_type,)).fetchall()
    #res = list(set(res))
    #print len(res)
    for id_group, id_word, isword in res:
      if R.dct_typesR[id_type] in ('abstract'): id_group = R.convert(id_group)[0]
      if isword == 0: id_word = R.convert(id_word)[0]
      if isword > 0: isword = R.dct_typesR[isword]
      else: isword = u'слово'
      print '  ', id_group, id_word, isword
  
  """list_words = ['dom', 'kot', 'kosxar', 'aparat', 'montr', 'sobak', 'peos']
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
  print R.get_commongroups('synonym', 'noun', [word, 0], [lst[1],0], [R.convert('aparat')[0], 0])"""
