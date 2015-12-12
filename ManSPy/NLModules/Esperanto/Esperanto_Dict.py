# -*- coding: utf-8 -*-
###############################################################################
dct = {

  'verb': {
    'end': {
      u'i': {'mood': 'infinitive'}, # инфинитив как вид наклонения - для удобства. 
      u'u': {'mood': 'imperative'},
      u'as': {'mood': 'indicative', 'tense': 'present'},
      u'is': {'mood': 'indicative', 'tense': 'past'},
      u'os': {'mood': 'indicative', 'tense': 'future'},
      u'us': {'mood': 'subjunctive'}
      },
    'base': [] # заполняются автоматически из пользовательских модулей
    },

  'noun': {
    'end': u'o',
    'base': []
    },

  'adverb': {
    'end': u'e',
    'base': [],
    'non-derivative': [   # непроизводные
      u'ankaŭ', u'hodiaŭ', u'tre', u'morgaŭ', u'nun', u'multe']
    },

  'adjective': {
    'end': u'a',
    'base': []
    },
  
  'pronoun': [u'li', u'mi', u'vi', u'ni', u'ili', u'ŝi', u'ĝi'],

  'preposition_d': {u'al': 'dative', u'da':'genetive', u'de':'genetive',
      u'en': 'locative', u'por': '', u'dum': '', u'inter': '', u'kun': '',
      u'el': 'ablative', u'sen': '', u'sur': '', u'per': 'instrumental',
      u'pri': '', u'ĉu': '', u'ĝis': ''},

  'conjunction_d': {'coordinating': [u'kaj', u'sed'], # сочинительные союзы
                    'subordinating': [] # подчинительные союзы
                    },

  'particle': [u'jes', u'ne', u'nur'],

  'article': [u'la'],

  'prefix': {'mal': {'antonym': True}},

  # порядок числительных НЕ МЕНЯТЬ!
  'numeral': [u'nulo', u'unu', u'du', u'tri', u'kvar', u'kvin',
    u'ses', u'sep', u'ok', u'naŭ', u'dek', u'cent', u'mil'],
  # а здесь можно, но не нужно :)
  'numeral_d': {u'nulo': 0, u'unu': 1, u'du': 2, u'tri': 3, u'kvar': 4, u'kvin': 5,
    u'ses': 6, u'sep': 7, u'ok': 8, u'naŭ': 9, u'dek': 10, u'cent': 100, u'mil': 1000
    }
  }

dct['preposition'] = dct['preposition_d'].keys()
dct['conjunction'] = dct['conjunction_d']['coordinating'] + dct['conjunction_d']['subordinating']

''' ĉ ĝ ĥ ĵ ŝ ŭ '''

'''L = ['a']
x = 0
for l in L:
  print len(L), len(l)     # Интересный код :)))))
  L.append(l+'a')
  x += 1
'''
