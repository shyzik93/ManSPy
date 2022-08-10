


signs = [
    # 'type' - Категория признака, 'value' - Значение признака, 'endow' - Наделяет свойством
    [
        # непроизводные наречия
        {'type': 'word', 'value': 'la', 'endow': {'POSpeech': 'article', 'value': 'defined'}},
        {'type': 'word', 'value': 'ankaŭ', 'endow': {'POSpeech': 'adverb'}},  # также, тоже, и (стоит непосредственно перед словыом, к которому относится)
        {'type': 'word', 'value': 'hodiaŭ', 'endow': {'POSpeech': 'adverb'}},  # сегодня
        {'type': 'word', 'value': 'tre', 'endow': {'POSpeech': 'adverb'}},  # очень
        {'type': 'word', 'value': 'morgaŭ', 'endow': {'POSpeech': 'adverb'}},  # завтра
        {'type': 'word', 'value': 'nun', 'endow': {'POSpeech': 'adverb'}},  # теперь, сейчас
        {'type': 'word', 'value': 'multe', 'endow': {'POSpeech': 'adverb'}},  # много
        {'type': 'word', 'value': 'ankoraŭ', 'endow': {'POSpeech': 'adverb'}},  # ещё
        {'type': 'word', 'value': 'jam', 'endow': {'POSpeech': 'adverb'}},  # уже
        {'type': 'word', 'value': 'certe', 'endow': {'POSpeech': 'adverb'}},  # уверенно, точно; конечно, несомненно, верно (прилагательное certa - уверенный, несомненный, определённый, точный)
        {'type': 'word', 'value': 'baldaŭ', 'endow': {'POSpeech': 'adverb'}},  # вскоре, скоро
        {'type': 'word', 'value': 'hieraŭ', 'endow': {'POSpeech': 'adverb'}},  # вчера
        {'type': 'word', 'value': 'neniam', 'endow': {'POSpeech': 'adverb'}},  # никогда
        {'type': 'word', 'value': 'apenaŭ', 'endow': {'POSpeech': 'adverb'}},  # едва, еле
        {'type': 'word', 'value': 'tuj', 'endow': {'POSpeech': 'adverb'}},  # сейчас, тотчас, сразу, немедленно
        {'type': 'word', 'value': 'nepre', 'endow': {'POSpeech': 'adverb'}},  # непременно, обязательно
        {'type': 'word', 'value': 'ĉiam', 'endow': {'POSpeech': 'adverb'}},  # всегда
        {'type': 'word', 'value': 'for', 'endow': {'POSpeech': 'adverb'}},  # прочь (прилагательное fora - далёкий)
        {'type': 'word', 'value': 'preskaŭ', 'endow': {'POSpeech': 'adverb'}},  # почти
        {'type': 'word', 'value': 'tro', 'endow': {'POSpeech': 'adverb'}},  # слишком
        # частицы
        {'type': 'word', 'value': 'jes', 'endow': {'POSpeech': 'particle'}},  # да
        {'type': 'word', 'value': 'ne', 'endow': {'POSpeech': 'particle'}},  # не, нет
        {'type': 'word', 'value': 'nur', 'endow': {'POSpeech': 'particle'}},  # только, (всего) лишь
        {'type': 'word', 'value': 'ĉu', 'endow': {'POSpeech': 'particle'}},  # ли (вопросительная)
        {'type': 'word', 'value': 'jen', 'endow': {'POSpeech': 'particle'}},  # вот (прилагательное jena - вот этот, следующий)
        {'type': 'word', 'value': 'eĉ', 'endow': {'POSpeech': 'particle'}},  # даже
        {'type': 'word', 'value': 'do', 'endow': {'POSpeech': 'particle'}},  # итак, следовательно, же
        {'type': 'word', 'value': 'nek', 'endow': {'POSpeech': 'particle'}},  # ни (употребляется в паре с некоторыми другими отрицательными словами)
        {'type': 'word', 'value': 'ĉi', 'endow': {'POSpeech': 'particle'}},  # обозначает близость
        # местоимения личные
        {'type': 'word', 'value': 'li', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  # он
        {'type': 'word', 'value': 'mi', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  # я
        {'type': 'word', 'value': 'vi', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  # ты, вы
        {'type': 'word', 'value': 'ni', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  # мы
        {'type': 'word', 'value': 'ŝi', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  # она
        {'type': 'word', 'value': 'ĝi', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  # неодушёвлённый, животное, или лица, пол которого неизвестен (он, оно, она)
        {'type': 'word', 'value': 'ili', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  # они
        # местоимения возвратные
        {'type': 'word', 'value': 'si', 'endow': {'case': 'nominative', 'category': 'reflexive'}},  # себя
        {'type': 'word', 'value': 'mem', 'endow': {'case': 'nominative', 'category': 'reflexive'}},  # сам
        # местоимения неопределённо-личные
        {'type': 'word', 'value': 'oni', 'endow': {'case': 'nominative', 'category': ''}},  # люди, многие, некто

        {'type': 'word', 'value': 'li', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  #
        {'type': 'word', 'value': 'li', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  #
        {'type': 'word', 'value': 'li', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  #
        {'type': 'word', 'value': 'li', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  #
        {'type': 'word', 'value': 'li', 'endow': {'POSpeech': 'pronoun', 'case': 'nominative', 'category': 'personal'}},  #
    ],
    [
        {'type': 'end', 'value': 'n', 'endow': {'case': 'accusative'}},
    ],
    [
        {'type': 'end', 'value': 'j', 'endow': {'number': 'plural'}},
    ],
    [
        {'type': 'end', 'value': 'i', 'endow': {'POSpeech': 'verb', 'mood': 'infinitive'}},
        {'type': 'end', 'value': 'u', 'endow': {'POSpeech': 'verb', 'mood': 'imperative'}},
        {'type': 'end', 'value': 'as', 'endow': {'POSpeech': 'verb', 'mood': 'indicative', 'tense': 'present'}},
        {'type': 'end', 'value': 'is', 'endow': {'POSpeech': 'verb', 'mood': 'indicative', 'tense': 'past'}},
        {'type': 'end', 'value': 'os', 'endow': {'POSpeech': 'verb', 'mood': 'infinitive', 'tense': 'future'}},
        {'type': 'end', 'value': 'us', 'endow': {'POSpeech': 'verb', 'mood': 'subjunctive'}},
        {'type': 'end', 'value': 'o', 'endow': {'POSpeech': 'noun'}},
        {'type': 'end', 'value': 'e', 'endow': {'POSpeech': 'adverb'}},
        {'type': 'end', 'value': 'a', 'endow': {'POSpeech': 'adjective'}},

        {'type': 'prefix', 'value': 'mal', 'endow': {'antonym': True}},

        {'type': 'case_of_first_letter', 'value': 'upper', 'endow': {'name': 'proper'}},
        {'type': 'case_of_first_letter', 'value': 'lower', 'endow': {'name': 'common'}},
    ],
    [
        {'type': 'prop-default', 'value': {'POSpeech': 'adjective'}, 'endow': {'number': 'singular', 'case': 'nominative', 'name': 'common2'}},
        {'type': 'prop-default', 'value': {'POSpeech': 'noun'}, 'endow': {'number': 'singular', 'case': 'nominative'}},
        {'type': 'prop', 'value': {'base': 'mi', 'POSpeech': 'adjective'}, 'endow': {'POSpeech': 'pronoun', 'category': 'possessive'}},  # притяжательное иестоимение
    ],
]

###############################################################################


dct = {
    # порядок числительных НЕ МЕНЯТЬ!
    'numeral': [u'nul', u'unu', u'du', u'tri', u'kvar', u'kvin',
        u'ses', u'sep', u'ok', u'naŭ', u'dek', u'cent', u'mil', u'milion', u'miliard'],
    # а здесь можно, но не нужно :)
    'numeral_d': {u'nul': 0, u'unu': 1, u'du': 2, u'tri': 3, u'kvar': 4, u'kvin': 5,
        u'ses': 6, u'sep': 7, u'ok': 8, u'naŭ': 9, u'dek': 10, u'cent': 100, u'mil': 1000, u'milion':1000000, u'miliard':1000000000
        }
    }

''' ĉ ĝ ĥ ĵ ŝ ŭ '''

words = {
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
        #u'do': {'value': ''}, # то (это частица)
        u'kvankam': {'value': ''}, # хотя
      },
    'numeral': {
        u'nul': {'class': 'cardinal', 'number_value': 0},
        u'unu':  {'class': 'cardinal', 'number_value': 1},
        u'du':   {'class': 'cardinal', 'number_value': 2},
        u'tri':  {'class': 'cardinal', 'number_value': 3},
        u'kvar': {'class': 'cardinal', 'number_value': 4},
        u'kvin': {'class': 'cardinal', 'number_value': 5},
        u'ses':  {'class': 'cardinal', 'number_value': 6},
        u'sep':  {'class': 'cardinal', 'number_value': 7},
        u'ok':   {'class': 'cardinal', 'number_value': 8},
        u'naŭ':  {'class': 'cardinal', 'number_value': 9},
        u'dek':  {'class': 'cardinal', 'number_value': 10},
        u'cent': {'class': 'cardinal', 'number_value': 100},
        u'mil':  {'class': 'cardinal', 'number_value': 1000},
        u'milion':  {'class': 'cardinal', 'number_value': 1000000},
        u'miliard': {'class': 'cardinal', 'number_value': 1000000000}
       }  
    }
