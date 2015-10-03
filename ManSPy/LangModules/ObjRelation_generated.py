# -*- coding: utf-8 -*-
from ObjRelation_new import _Relation

class Relation(_Relation):
  dct_types = {'synonym': 0, 'antonym': 1, 'abstract': 2}
  dct_speeches = {'noun': 0, 'verb': 1, 'adjective': 2, 'adverb': 3}
  def __init__(self, language):
    _Relation.__init__(self, language)

  def add_idwords_to_group(self, _type, speech, id_group, isword, *words):
    id_type = self.id_types[_type]
    id_speech = self.id_speeches[speech]
    id_words = _Relation.word_to_id(*words)
    id_group = Relation._add_idwords_to_group(self, id_type, id_speech, id_group, isword, *id_words)
    return id_group

  def get_idgroups_by_idword(self, isword, word, id_type=None, id_speech=None):
    id_word = _Relation._word_to_id(word)
    id_groups = Relation._get_idgroups_by_idword(self, isword, id_word, id_type, id_speech)
    return id_groups

  def get_idwords_by_idgroup(self, id_group, isword, id_type=None, id_speech=None):
    id_words = Relation._get_idwords_by_idgroup(self, id_group, isword, id_type, id_speech)
    words = _Relation.id_to_word(*id_words)
    return words

  def add_idwords_to_same_group(self, _type, speech, isword, word, *words):
    id_type = self.id_types[_type]
    id_speech = self.id_speeches[speech]
    id_word = _Relation._word_to_id(word)
    id_words = _Relation.word_to_id(*words)
    Relation._add_idwords_to_same_group(self, id_type, id_speech, isword, id_word, *id_words)

  def get_idwords_from_same_group(self, _type, speech, isword, word):
    id_type = self.id_types[_type]
    id_speech = self.id_speeches[speech]
    id_word = _Relation._word_to_id(word)
    id_words = Relation._get_idwords_from_same_group(self, id_type, id_speech, isword, id_word)
    words = _Relation.id_to_word(*id_words)
    return words

  def is_idword_in_group(self, id_group, word, isword, id_type=None, id_speech=None):
    id_word = _Relation._word_to_id(word)
    return Relation._is_idword_in_group(self, id_group, id_word, isword, id_type, id_speech)

  def get_same_groups(self, _type, speech, *pairs):
    id_type = self.id_types[_type]
    id_speech = self.id_speeches[speech]
    for pair in pairs: pair[0] = _Relation._word_to_id(pair[0]) #*pairs
    id_groups = Relation._get_same_groups(self, id_type, id_speech, *pairs)
    return id_groups

if __name__ == '__main__':
  R = Relation('Esperanto')
  R.add_word('montr', 'rubl')
  print R.id_to_word(1, 2)
