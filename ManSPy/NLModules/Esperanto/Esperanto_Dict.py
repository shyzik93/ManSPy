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
  'adverb':  { # непроизводные
    u'ankaŭ':  {}, # также, тоже, и (стоит непосредственно перед словыом, к которому относится)
    u'hodiaŭ': {}, # сегодня
    u'tre':    {}, # очень
    u'morgaŭ': {}, # завтра
    u'nun':    {}, # теперь, сейчас
    u'multe':  {}, # много
    u'ankoraŭ':{}, # ещё
    u'jam':    {}, # уже
    u'certe':  {}, # уверенно, точно; конечно, несомненно, верно (прилагательное certa - уверенный, несомненный, определённый, точный)
    u'baldaŭ': {}, # вскоре, скоро
    u'hieraŭ': {}, # вчера
    u'neniam': {},  # никогда
    u'apenaŭ': {}, # едва, еле
    u'tuj': {}, # сейчас, тотчас, сразу, немедленно
    u'nepre': {}, # непременно, обязательно
    u'ĉiam': {}, # всегда
    u'for': {}, # прочь (прилагательное fora - далёкий)
    u'preskaŭ': {}, # почти
    u'tro': {}, # слишком
    },
  'particle': {
    u'jes':{},# да
    u'ne':{}, # не, нет
    u'nur':{},# только, (всего) лишь
    u'ĉu':{}, # ли (вопросительная)
    u'jen':{},# вот (прилагательное jena - вот этот, следующий)
    u'eĉ':{},  # даже
    u'do':{},  # итак, следовательно, же
    u'nek':{},  # ни (употребляется в паре с некоторыми другими отрицательными словами)
    u'ĉi':{},  # обозначает близость
    },
  'article': {u'la': {'value': 'defined'}},
  'pronoun': {
    # личные
    u'li':  {'case': 'nominative', 'category': 'personal'}, # он
    u'mi':  {'case': 'nominative', 'category': 'personal'}, # я
    u'vi':  {'case': 'nominative', 'category': 'personal'}, # ты, вы
    u'ni':  {'case': 'nominative', 'category': 'personal'}, # мы
    u'ŝi':  {'case': 'nominative', 'category': 'personal'}, # она
    u'ĝi':  {'case': 'nominative', 'category': 'personal'}, # неодушёвлённый, животное, или лица, пол которого неизвестен (он, оно, она)
    u'ili': {'case': 'nominative', 'category': 'personal'}, # они
    # возвратное
    u'si': {'case': 'nominative', 'category': 'reflexive'}, # себя
    u'mem': {'case': 'nominative', 'category': 'reflexive'}, # сам
    # неопределённо-личные
    u'oni': {'case': 'nominative', 'category': ''}, # люди, многие, некто
    },
  'preposition': {
    u'je':    {'give_case': 'undefined'},# с неопределённым значкением. Употребляется, когда не ясно, какой предлог использовать (Je via sano! - За ваше здоровье!)
    u'al':    {'give_case': 'dative'},   # к. Или не переводится (дательный падеж) (направление движения к цели)
    u'da':    {'give_case': 'genetive'}, # не переводится (русский родительный падеж). для чего(кого)-либо не имеющих чётких границ для разделения (жидкости, материалы)
    u'de':    {'give_case': 'genetive'}, # не переводится (русский родительный падеж)
    u'en':    {'give_case': 'locative'}, # в
    u'el':    {'give_case': 'ablative'}, # из
    u'ĉe':    {'give_case': ''}, # у, при
    u'por':   {'give_case': ''}, # для, за, с целью, для того чтобы
    u'dum':   {'give_case': ''}, # во время, в течение, пока, в то время как (производное наречие dume - тем временем, пока)
    u'kun':   {'give_case': ''}, # с
    u'sen':   {'give_case': ''}, # без
    u'sur':   {'give_case': ''}, # на
    u'per':   {'give_case': 'instrumental'}, # не перводится, но иногда: посредством, с помощью (творительный падеж)
    u'pri':   {'give_case': ''}, # о
    u'tra':   {'give_case': ''}, # через, сквозь (направление движения к цели)
    u'ĝis':   {'give_case': 'dative'}, # до (направление движения к цели)
    u'post':  {'give_case': ''}, # после, через, за
    u'inter': {'give_case': ''}, # между, среди
    u'antaŭ': {'give_case': ''}, # перед
    u'ĉirkaŭ': {'give_case': ''}, # вокруг
    u'sub':   {'give_case': ''}, # под
    u'ekster':   {'give_case': ''}, # вне, за
    u'apud':   {'give_case': ''}, # около, возле
    u'trans':   {'give_case': ''}, # за, через, по ту сторону
    u'super':   {'give_case': ''}, # над
    u'kontraŭ':   {'give_case': ''}, # против, о
    # составной предлог (вероятно, выделять через отдельную функцию. Хранить в отдельном словаре)
    u'okaze de':   {'give_case': ''}, # по случаю
    # выражают локативные, временные, субъектно-объектные отношения составными предлогами (ekdi, pere de, dank' al, de sur и т. д.)
    },
  'conjunction': {
    u'kaj': {'value': 'coordinating'}, # и, а # сочинительные союзы
    u'sed': {'value': 'coordinating'}, # но, а
    u'aŭ': {'value': 'coordinating'},  # или, либо
    u'ke': {'value': 'subordinating'}, # что, чтобы (с помощью него дополнительное придаточное предложение присоединяется к главному - Li diris, ke li lernis la lecionon)# подчинительные союзы
    u'ĉar': {'value': 'subordinating'}, # потому что, так как, поскольку, ибо # подчинительные союзы
    # es ... (do). Если ... (то)
    u'se': {'value': ''}, # если
    u'do': {'value': ''}, # то
    u'kvankam': {'value': ''}, # хотя
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
