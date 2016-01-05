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
    },

  'noun': { 'end': u'o', },

  'adverb': { 'end': u'e', },

  'adjective': { 'end': u'a', },

  'prefix': {'mal': {'antonym': True}},

  # порядок числительных НЕ МЕНЯТЬ!
  'numeral': [u'nulo', u'unu', u'du', u'tri', u'kvar', u'kvin',
    u'ses', u'sep', u'ok', u'naŭ', u'dek', u'cent', u'mil'],
  # а здесь можно, но не нужно :)
  'numeral_d': {u'nulo': 0, u'unu': 1, u'du': 2, u'tri': 3, u'kvar': 4, u'kvin': 5,
    u'ses': 6, u'sep': 7, u'ok': 8, u'naŭ': 9, u'dek': 10, u'cent': 100, u'mil': 1000
    }
  }

''' ĉ ĝ ĥ ĵ ŝ ŭ '''

morphemes = {
  }

words = {
  'adverb':  {u'ankaŭ':{}, u'hodiaŭ':{}, u'tre':{}, u'morgaŭ':{}, u'nun':{}, u'multe':{}, u'ankoraŭ':{}, u'jam':{}, u'certe':{}, u'baldaŭ':{}, u'hieraŭ':{}, u'neniam':{}}, # непроизводные
  'particle': {u'jes':{}, u'ne':{}, u'nur':{}, u'ĉu':{}, u'jen':{}, u'eĉ':{}},
  'article': {u'la': {'value': 'defined'}},
  'pronoun': {
    u'li':  {'case': 'nominative', 'category': 'personal'},
    u'mi':  {'case': 'nominative', 'category': 'personal'},
    u'vi':  {'case': 'nominative', 'category': 'personal'},
    u'ni':  {'case': 'nominative', 'category': 'personal'},
    u'ŝi':  {'case': 'nominative', 'category': 'personal'},
    u'ĝi':  {'case': 'nominative', 'category': 'personal'},
    u'ili': {'case': 'nominative', 'category': 'personal'},
    },
  'preposition': {
    u'je':    {'give_case': 'undefined'}, # употребляется, когда не ясно, какой предлог использовать (Je via sano! - За ваше здоровье!)
    u'al':    {'give_case': 'dative'},
    u'da':    {'give_case': 'genetive'},
    u'de':    {'give_case': 'genetive'},
    u'en':    {'give_case': 'locative'},
    u'el':    {'give_case': 'ablative'},
    u'ĉe':    {'give_case': ''},
    u'por':   {'give_case': ''},
    u'dum':   {'give_case': ''},
    u'kun':   {'give_case': ''},
    u'sen':   {'give_case': ''},
    u'sur':   {'give_case': ''},
    u'per':   {'give_case': 'instrumental'},
    u'pri':   {'give_case': ''},
    u'tra':   {'give_case': ''},
    u'ĝis':   {'give_case': ''},
    u'post':  {'give_case': ''},
    u'inter': {'give_case': ''},
    u'antaŭ': {'give_case': ''},
    u'ĉirkaŭ': {'give_case': ''}
    },
  'conjunction': {
    u'kaj': {'value': 'coordinating'}, # и # сочинительные союзы
    u'sed': {'value': 'coordinating'}, # но, да, а
    u'aŭ': {'value': 'coordinating'}, # или, либо
    u'ke': {'value': 'subordinating'}, # что # подчинительные союзы
    u'ĉar': {'value': 'subordinating'} # потому что, так как, поскольку, ибо # подчинительные союзы
    },
  'numeral': {
    u'nulo': {'class': 'cardinal', 'figure': 0},
    u'unu':  {'class': 'cardinal', 'figure': 1},
    u'du':   {'class': 'cardinal', 'figure': 2},
    u'tri':  {'class': 'cardinal', 'figure': 3},
    u'kvar': {'class': 'cardinal', 'figure': 4},
    u'kvin': {'class': 'cardinal', 'figure': 5},
    u'ses':  {'class': 'cardinal', 'figure': 6},
    u'sep':  {'class': 'cardinal', 'figure': 7},
    u'ok':   {'class': 'cardinal', 'figure': 8},
    u'naŭ':  {'class': 'cardinal', 'figure': 9},
    u'dek':  {'class': 'cardinal', 'figure': 10},
    u'cent': {'class': 'cardinal', 'figure': 100},
    u'mil':  {'class': 'cardinal', 'figure': 1000}
    }  
  }
