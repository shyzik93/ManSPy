# -*- coding:utf-8 -*-
from pprint import pprint
from ManSPy import LangModules, Action
import pickle, copy, time, json

settings = {'history': 1,
              'monitor': 1, # включает вывод на экран статистику работы ИСУ
              'logic': 1, # включает модуль логики
              'convert2IL': 1, # включает последний этап конвертации
                               # если при отключении включёна логика, то будет ошибка
              'language': 'Esperanto',
              'storage_version': 2,
              'converter_version': 1,
              'test': True, # тестовый режим, включаемый в процессе отладки и разработки
              'dir_db': None
  }
LC = LangModules.LangClass(settings, Action)

def copy_word(dct_word, absent=[]):
  _dct_word = {}
  for characteristic, value in dct_word.items():
    if characteristic not in ['MOSentence', 'POSpeech', 'case', 'feature', 'base']: continue
    if characteristic in absent: continue # absent - те характеристики, которые должны исключится из списка нужных
    if characteristic == 'feature':
      value = copy.deepcopy(value)
      for fea_index, fea_word in enumerate(value):
        value[fea_index] = copy_word(fea_word, ['case', 'POSpeech'])
    _dct_word[characteristic] = value
  return _dct_word

def to_hash(dct_sentence):
  dct_sentence = word_combination.getUnit('dict', 'members', 'info')
  _dct_sentence = {}

  # падеж и член предложения первого чдена не учитывается (они могут иметь разные падежи членства)
  _dct_sentence[0] = copy_word(dct_sentence[0], ['case', 'MOSentence'])

  for index, dct_word in dct_sentence.items()[1:]:
    _dct_sentence[index] = copy_word(dct_word)

  #pprint(_dct_sentence, indent=4)

  json_sentence = json.dumps(_dct_sentence,  sort_keys=True)
  return hash(json_sentence), json_sentence
'''
-1965140811
2003176567
-1965140811
'''
word_combinations = [
  "dolara cambio de rusia kaj ukrainia banko",
  "dolara cambio de rusia banko",
  "dolaran cambion de rusia kaj ukrainia banko"]
for word_combination in word_combinations:
  word_combination = LC.NL2IL(word_combination, ":synt")[0][0]
  #pprint(word_combination.getSentence('dict'), indent=4)
  print to_hash(word_combination.getUnit('dict', 'members', 'info'))[0]
