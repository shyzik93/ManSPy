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
        # предлоги
        {'type': 'word', 'value': 'je', 'endow': {'POSpeech': 'preposition', 'give_case': 'undefined'}},  # с неопределённым значением. Употребляется, когда не ясно, какой предлог использовать (Je via sano! - За ваше здоровье!)
        {'type': 'word', 'value': 'al', 'endow': {'POSpeech': 'preposition', 'give_case': 'dative'}},  # к. Или не переводится (дательный падеж) (направление движения к цели)
        {'type': 'word', 'value': 'da', 'endow': {'POSpeech': 'preposition', 'give_case': 'genetive'}},  # не переводится (русский родительный падеж). для чего(кого)-либо не имеющих чётких границ для разделения (жидкости, материалы)
        {'type': 'word', 'value': 'de', 'endow': {'POSpeech': 'preposition', 'give_case': 'genetive'}},  # не переводится (русский родительный падеж)
        {'type': 'word', 'value': 'en', 'endow': {'POSpeech': 'preposition', 'give_case': 'locative'}},  # в
        {'type': 'word', 'value': 'el', 'endow': {'POSpeech': 'preposition', 'give_case': 'ablative'}},  # из
        {'type': 'word', 'value': 'ĉe', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # у, при
        {'type': 'word', 'value': 'por', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # для, за, с целью, для того чтобы
        {'type': 'word', 'value': 'dum', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # во время, в течение, пока, в то время как (производное наречие dume - тем временем, пока)
        {'type': 'word', 'value': 'kun', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # с
        {'type': 'word', 'value': 'sen', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # без
        {'type': 'word', 'value': 'sur', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # на
        {'type': 'word', 'value': 'per', 'endow': {'POSpeech': 'preposition', 'give_case': 'instrumental'}},  # не перводится, но иногда: посредством, с помощью (творительный падеж)
        {'type': 'word', 'value': 'pri', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # о
        {'type': 'word', 'value': 'tra', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # через, сквозь (направление движения к цели)
        {'type': 'word', 'value': 'ĝis', 'endow': {'POSpeech': 'preposition', 'give_case': 'dative'}},  # до (направление движения к цели)
        {'type': 'word', 'value': 'post', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # после, через, за
        {'type': 'word', 'value': 'inter', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # между, среди
        {'type': 'word', 'value': 'antaŭ', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # перед
        {'type': 'word', 'value': 'ĉirkaŭ', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # вокруг
        {'type': 'word', 'value': 'sub', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # под
        {'type': 'word', 'value': 'ekster', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # вне, за
        {'type': 'word', 'value': 'apud', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # около, возле
        {'type': 'word', 'value': 'trans', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # за, через, по ту сторону
        {'type': 'word', 'value': 'super', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # над
        {'type': 'word', 'value': 'kontraŭ', 'endow': {'POSpeech': 'preposition', 'give_case': ''}},  # против, о
        # союзы
        {'type': 'word', 'value': 'kaj', 'endow': {'POSpeech': 'conjunction', 'value': 'coordinating'}},  # и, а # сочинительные союзы
        {'type': 'word', 'value': 'sed', 'endow': {'POSpeech': 'conjunction', 'value': 'coordinating'}},  # но, а
        {'type': 'word', 'value': 'aŭ', 'endow': {'POSpeech': 'conjunction', 'value': 'coordinating'}},  # или, либо
        {'type': 'word', 'value': 'ke', 'endow': {'POSpeech': 'conjunction', 'value': 'subordinating'}},  # что, чтобы (с помощью него дополнительное придаточное предложение присоединяется к главному - Li diris, ke li lernis la lecionon)# подчинительные союзы
        {'type': 'word', 'value': 'ĉar', 'endow': {'POSpeech': 'conjunction', 'value': 'subordinating'}},  # потому что, так как, поскольку, ибо # подчинительные союзы
        {'type': 'word', 'value': 'se', 'endow': {'POSpeech': 'conjunction', 'value': ''}},  # если
        {'type': 'word', 'value': 'kvankam', 'endow': {'POSpeech': 'conjunction', 'value': ''}},  # хотя
    ],
    [
        {'type': 'end', 'value': 'n', 'endow': {'case': 'accusative'}, 'if-not': {'POSpeech': 'preposition'}},
    ],
    [
        {'type': 'end', 'value': 'j', 'endow': {'number': 'plural'}, 'if-not': {'POSpeech': 'conjunction'}},
    ],
    [
        {'type': 'end', 'value': 'i', 'endow': {'POSpeech': 'verb', 'mood': 'infinitive'}},
        {'type': 'end', 'value': 'u', 'endow': {'POSpeech': 'verb', 'mood': 'imperative'}},
        {'type': 'end', 'value': 'as', 'endow': {'POSpeech': 'verb', 'mood': 'indicative', 'tense': 'present'}},
        {'type': 'end', 'value': 'is', 'endow': {'POSpeech': 'verb', 'mood': 'indicative', 'tense': 'past'}},
        {'type': 'end', 'value': 'os', 'endow': {'POSpeech': 'verb', 'mood': 'infinitive', 'tense': 'future'}},
        {'type': 'end', 'value': 'us', 'endow': {'POSpeech': 'verb', 'mood': 'subjunctive'}},
        {'type': 'end', 'value': 'o', 'endow': {'POSpeech': 'noun'}},
        {'type': 'end', 'value': 'e', 'endow': {'POSpeech': 'adverb'}, 'if-not': {'POSpeech': 'preposition'}},
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

numeral_list = [  # порядок числительных НЕ МЕНЯТЬ!
    'nul', 'unu', 'du', 'tri', 'kvar', 'kvin', 'ses', 'sep', 'ok', 'naŭ', 'dek', 'cent', 'mil', 'milion', 'miliard',
]
numeral_dict = {
    'nul': 0, 'unu': 1, 'du': 2, 'tri': 3, 'kvar': 4, 'kvin': 5, 'ses': 6, 'sep': 7, 'ok': 8, 'naŭ': 9, 'dek': 10,
    'cent': 100, 'mil': 1000, 'milion': 1000000, 'miliard': 1000000000,
}

''' ĉ ĝ ĥ ĵ ŝ ŭ '''

words = {
        # предлоги
        # составной предлог (вероятно, выделять через отдельную функцию. Хранить в отдельном словаре)
        # u'okaze de':   {'give_case': ''}, # по случаю
        # выражают локативные, временные, субъектно-объектные отношения составными предлогами (ekdi, pere de, dank' al, de sur и т. д.)

        # союз es ... (do). Если ... (то)
        #u'do': {'value': ''}, # то (это частица)
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
