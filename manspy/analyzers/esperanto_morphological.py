"""
Модуль выполняет стандартный морфологический анализ слова ЕЯ Эсперанто,
основывваясь только на морфологических признаках (на внешнем виде слова)

Нерешённые вопросы:
    # предлоги
    # составной предлог (вероятно, выделять через отдельную функцию. Хранить в отдельном словаре)
    # u'okaze de':   {'give_case': ''}, # по случаю
    # выражают локативные, временные, субъектно-объектные отношения составными предлогами (ekdi, pere de, dank' al, de sur и т. д.)

    # союз es ... (do). Если ... (то)
    #u'do': {'value': ''}, # то (это частица)

    # ERROR слово prezenten и enden определяется наречием. Другие слова на -n могут ошибочно определиться.

Esperanto some letters: ĉ ĝ ĥ ĵ ŝ ŭ

Какой-то текст:
    #sentence = 'vi montru kursojn de mia dolaro'
    #sentence = '1444 123.78654 345,976 0.7 9,8'
    #sentence = 'triA unu Tridek kvarcent du mil'
"""
import re

from manspy.utils.constants import (
    ADJECTIVE, ADVERB, ARTICLE,
    CASE, COMMON, CONJUNCTION, COORDINATING,
    GENETIVE,
    NAME, NOMINATIVE, NOUN, NUMERAL,
    PARTICLE, POSPEECH, PREPOSITION, PRONOUN, PROPER,
    SUBORDINATING,
    VALUE, VERB,
)


numeral_dict = {  # порядок числительных НЕ МЕНЯТЬ!
    'nul': 0, 'unu':  1, 'du':   2, 'tri':  3, 'kvar': 4, 'kvin': 5, 'ses':  6, 'sep':  7, 'ok':   8, 'naŭ':  9,
    'dek':  10, 'cent': 100, 'mil':  1000, 'milion':  1000000, 'miliard': 1000000000,
}
numeral_list = list(numeral_dict.keys())
combain_numerals_template = re.compile(
    '^({})({}|{})$'.format(
        '|'.join(numeral_list[:10]),
        numeral_list[10],
        numeral_list[11],
    )
)
mili_numerals_template = re.compile('^({})(iliard|ilion)$'.format('|'.join(numeral_list[:10])))


def is_numeral(word):
    word_l = word['base']
    if word_l in numeral_dict:
        word['number_value'] = numeral_dict[word_l]
        return True

    combain_numerals = combain_numerals_template.findall(word_l)
    if combain_numerals:
        factor1, factor2 = combain_numerals[0]
        word['number_value'] = numeral_dict[factor2] * numeral_dict[factor1]
        return True

    mili_numerals = mili_numerals_template.findall(word_l)
    if mili_numerals:
        factor1, factor2 = mili_numerals[0]
        word['number_value'] = numeral_dict['milion'] ** numeral_dict[factor1]
        if factor2 == 'iliard':
            word['number_value'] *= 1000

        return True

    return False


def convert_figure(word):
    word['number_value'] = float(word['word_lower'].replace(',', '.'))

signs = [
    # 'type' - Категория признака, 'value' - Значение признака, 'endow' - Наделяет свойством
    [
        # непроизводные наречия
        {'type': 'word', 'value': 'la', 'endow': {POSPEECH: ARTICLE, 'value': 'defined'}},
        {'type': 'word', 'value': 'ankaŭ', 'endow': {POSPEECH: ADVERB}},  # также, тоже, и (стоит непосредственно перед словыом, к которому относится)
        {'type': 'word', 'value': 'hodiaŭ', 'endow': {POSPEECH: ADVERB}},  # сегодня
        {'type': 'word', 'value': 'tre', 'endow': {POSPEECH: ADVERB}},  # очень
        {'type': 'word', 'value': 'morgaŭ', 'endow': {POSPEECH: ADVERB}},  # завтра
        {'type': 'word', 'value': 'nun', 'endow': {POSPEECH: ADVERB}},  # теперь, сейчас
        {'type': 'word', 'value': 'multe', 'endow': {POSPEECH: ADVERB}},  # много
        {'type': 'word', 'value': 'ankoraŭ', 'endow': {POSPEECH: ADVERB}},  # ещё
        {'type': 'word', 'value': 'jam', 'endow': {POSPEECH: ADVERB}},  # уже
        {'type': 'word', 'value': 'certe', 'endow': {POSPEECH: ADVERB}},  # уверенно, точно; конечно, несомненно, верно (прилагательное certa - уверенный, несомненный, определённый, точный)
        {'type': 'word', 'value': 'baldaŭ', 'endow': {POSPEECH: ADVERB}},  # вскоре, скоро
        {'type': 'word', 'value': 'hieraŭ', 'endow': {POSPEECH: ADVERB}},  # вчера
        {'type': 'word', 'value': 'neniam', 'endow': {POSPEECH: ADVERB}},  # никогда
        {'type': 'word', 'value': 'apenaŭ', 'endow': {POSPEECH: ADVERB}},  # едва, еле
        {'type': 'word', 'value': 'tuj', 'endow': {POSPEECH: ADVERB}},  # сейчас, тотчас, сразу, немедленно
        {'type': 'word', 'value': 'nepre', 'endow': {POSPEECH: ADVERB}},  # непременно, обязательно
        {'type': 'word', 'value': 'ĉiam', 'endow': {POSPEECH: ADVERB}},  # всегда
        {'type': 'word', 'value': 'for', 'endow': {POSPEECH: ADVERB}},  # прочь (прилагательное fora - далёкий)
        {'type': 'word', 'value': 'preskaŭ', 'endow': {POSPEECH: ADVERB}},  # почти
        {'type': 'word', 'value': 'tro', 'endow': {POSPEECH: ADVERB}},  # слишком
        # частицы
        {'type': 'word', 'value': 'jes', 'endow': {POSPEECH: PARTICLE}},  # да
        {'type': 'word', 'value': 'ne', 'endow': {POSPEECH: PARTICLE}},  # не, нет
        {'type': 'word', 'value': 'nur', 'endow': {POSPEECH: PARTICLE}},  # только, (всего) лишь
        {'type': 'word', 'value': 'ĉu', 'endow': {POSPEECH: PARTICLE}},  # ли (вопросительная)
        {'type': 'word', 'value': 'jen', 'endow': {POSPEECH: PARTICLE}},  # вот (прилагательное jena - вот этот, следующий)
        {'type': 'word', 'value': 'eĉ', 'endow': {POSPEECH: PARTICLE}},  # даже
        {'type': 'word', 'value': 'do', 'endow': {POSPEECH: PARTICLE}},  # итак, следовательно, же
        {'type': 'word', 'value': 'nek', 'endow': {POSPEECH: PARTICLE}},  # ни (употребляется в паре с некоторыми другими отрицательными словами)
        {'type': 'word', 'value': 'ĉi', 'endow': {POSPEECH: PARTICLE}},  # обозначает близость
        # местоимения личные
        {'type': 'word', 'value': 'li', 'endow': {POSPEECH: PRONOUN, CASE: NOMINATIVE, 'category': 'personal'}},  # он
        {'type': 'word', 'value': 'mi', 'endow': {POSPEECH: PRONOUN, CASE: NOMINATIVE, 'category': 'personal'}},  # я
        {'type': 'word', 'value': 'vi', 'endow': {POSPEECH: PRONOUN, CASE: NOMINATIVE, 'category': 'personal'}},  # ты, вы
        {'type': 'word', 'value': 'ni', 'endow': {POSPEECH: PRONOUN, CASE: NOMINATIVE, 'category': 'personal'}},  # мы
        {'type': 'word', 'value': 'ŝi', 'endow': {POSPEECH: PRONOUN, CASE: NOMINATIVE, 'category': 'personal'}},  # она
        {'type': 'word', 'value': 'ĝi', 'endow': {POSPEECH: PRONOUN, CASE: NOMINATIVE, 'category': 'personal'}},  # неодушёвлённый, животное, или лица, пол которого неизвестен (он, оно, она)
        {'type': 'word', 'value': 'ili', 'endow': {POSPEECH: PRONOUN, CASE: NOMINATIVE, 'category': 'personal'}},  # они
        # местоимения возвратные
        {'type': 'word', 'value': 'si', 'endow': {CASE: NOMINATIVE, 'category': 'reflexive'}},  # себя
        {'type': 'word', 'value': 'mem', 'endow': {CASE: NOMINATIVE, 'category': 'reflexive'}},  # сам
        # местоимения неопределённо-личные
        {'type': 'word', 'value': 'oni', 'endow': {CASE: NOMINATIVE, 'category': ''}},  # люди, многие, некто
        # предлоги
        {'type': 'word', 'value': 'je', 'endow': {POSPEECH: PREPOSITION, 'give_case': 'undefined'}},  # с неопределённым значением. Употребляется, когда не ясно, какой предлог использовать (Je via sano! - За ваше здоровье!)
        {'type': 'word', 'value': 'al', 'endow': {POSPEECH: PREPOSITION, 'give_case': 'dative'}},  # к. Или не переводится (дательный падеж) (направление движения к цели)
        {'type': 'word', 'value': 'da', 'endow': {POSPEECH: PREPOSITION, 'give_case': GENETIVE}},  # не переводится (русский родительный падеж). для чего(кого)-либо не имеющих чётких границ для разделения (жидкости, материалы)
        {'type': 'word', 'value': 'de', 'endow': {POSPEECH: PREPOSITION, 'give_case': GENETIVE}},  # не переводится (русский родительный падеж)
        {'type': 'word', 'value': 'en', 'endow': {POSPEECH: PREPOSITION, 'give_case': 'locative'}},  # в
        {'type': 'word', 'value': 'el', 'endow': {POSPEECH: PREPOSITION, 'give_case': 'ablative'}},  # из
        {'type': 'word', 'value': 'ĉe', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # у, при
        {'type': 'word', 'value': 'por', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # для, за, с целью, для того чтобы
        {'type': 'word', 'value': 'dum', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # во время, в течение, пока, в то время как (производное наречие dume - тем временем, пока)
        {'type': 'word', 'value': 'kun', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # с
        {'type': 'word', 'value': 'sen', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # без
        {'type': 'word', 'value': 'sur', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # на
        {'type': 'word', 'value': 'per', 'endow': {POSPEECH: PREPOSITION, 'give_case': 'instrumental'}},  # не перводится, но иногда: посредством, с помощью (творительный падеж)
        {'type': 'word', 'value': 'pri', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # о
        {'type': 'word', 'value': 'tra', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # через, сквозь (направление движения к цели)
        {'type': 'word', 'value': 'ĝis', 'endow': {POSPEECH: PREPOSITION, 'give_case': 'dative'}},  # до (направление движения к цели)
        {'type': 'word', 'value': 'post', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # после, через, за
        {'type': 'word', 'value': 'inter', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # между, среди
        {'type': 'word', 'value': 'antaŭ', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # перед
        {'type': 'word', 'value': 'ĉirkaŭ', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # вокруг
        {'type': 'word', 'value': 'sub', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # под
        {'type': 'word', 'value': 'ekster', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # вне, за
        {'type': 'word', 'value': 'apud', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # около, возле
        {'type': 'word', 'value': 'trans', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # за, через, по ту сторону
        {'type': 'word', 'value': 'super', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # над
        {'type': 'word', 'value': 'kontraŭ', 'endow': {POSPEECH: PREPOSITION, 'give_case': ''}},  # против, о
        # союзы
        {'type': 'word', 'value': 'kaj', 'endow': {POSPEECH: CONJUNCTION, VALUE: COORDINATING}},  # и, а # сочинительные союзы
        {'type': 'word', 'value': 'sed', 'endow': {POSPEECH: CONJUNCTION, VALUE: COORDINATING}},  # но, а
        {'type': 'word', 'value': 'aŭ', 'endow': {POSPEECH: CONJUNCTION, VALUE: COORDINATING}},  # или, либо
        {'type': 'word', 'value': 'ke', 'endow': {POSPEECH: CONJUNCTION, VALUE: SUBORDINATING}},  # что, чтобы (с помощью него дополнительное придаточное предложение присоединяется к главному - Li diris, ke li lernis la lecionon)# подчинительные союзы
        {'type': 'word', 'value': 'ĉar', 'endow': {POSPEECH: CONJUNCTION, VALUE: SUBORDINATING}},  # потому что, так как, поскольку, ибо # подчинительные союзы
        {'type': 'word', 'value': 'se', 'endow': {POSPEECH: CONJUNCTION, VALUE: ''}},  # если
        {'type': 'word', 'value': 'kvankam', 'endow': {POSPEECH: CONJUNCTION, VALUE: ''}},  # хотя
        # числительные
        {'type': 'function', 'value': is_numeral, 'endow': {'_isnumeral': 'yes'}},
        {'type': 'prop-update', 'value': {'_isnumeral': 'yes'}, 'endow': {POSPEECH: NUMERAL, 'class': 'cardinal'}},
    ],
    [
        {'type': 'end', 'value': 'n', 'endow': {CASE: 'accusative'}, 'if-not': [{POSPEECH: PREPOSITION}]},
    ],
    [
        {'type': 'end', 'value': 'j', 'endow': {'number': 'plural'}, 'if-not': [{POSPEECH: CONJUNCTION}]},
    ],
    [
        {'type': 'end', 'value': 'i', 'endow': {POSPEECH: VERB, 'mood': 'infinitive'}, 'if-not': [{POSPEECH: NUMERAL}]},
        {'type': 'end', 'value': 'u', 'endow': {POSPEECH: VERB, 'mood': 'imperative'}},
        {'type': 'end', 'value': 'as', 'endow': {POSPEECH: VERB, 'mood': 'indicative', 'tense': 'present'}},
        {'type': 'end', 'value': 'is', 'endow': {POSPEECH: VERB, 'mood': 'indicative', 'tense': 'past'}},
        {'type': 'end', 'value': 'os', 'endow': {POSPEECH: VERB, 'mood': 'infinitive', 'tense': 'future'}},
        {'type': 'end', 'value': 'us', 'endow': {POSPEECH: VERB, 'mood': 'subjunctive'}},
        {'type': 'end', 'value': 'o', 'endow': {POSPEECH: NOUN}},
        {'type': 'end', 'value': 'e', 'endow': {POSPEECH: ADVERB}, 'if-not': [{POSPEECH: PREPOSITION}]},
        {'type': 'end', 'value': 'a', 'endow': {POSPEECH: ADJECTIVE}},

        {'type': 'prefix', 'value': 'mal', 'endow': {'antonym': True}},

        {'type': 'case_of_first_letter', 'value': 'upper', 'endow': {NAME: PROPER}},
        {'type': 'case_of_first_letter', 'value': 'lower', 'endow': {NAME: COMMON}},
    ],
    [
        {'type': 'prop-default', 'value': {POSPEECH: ADJECTIVE}, 'endow': {'number': 'singular', CASE: NOMINATIVE, NAME: 'common2'}},
        {'type': 'prop-default', 'value': {POSPEECH: NOUN}, 'endow': {'number': 'singular', CASE: NOMINATIVE}},
        {'type': 'prop-update', 'value': {'base': 'mi', POSPEECH: ADJECTIVE}, 'endow': {POSPEECH: PRONOUN, 'category': 'possessive'}},  # притяжательное иестоимение
    ],
    [
        {'type': 'function-update', 'value': is_numeral, 'endow': {'_isnumeral': 'yes'}},
        {'type': 'prop-update', 'value': {'_isnumeral': 'yes', POSPEECH: ADJECTIVE}, 'endow': {POSPEECH: NUMERAL, 'class': 'ordinal'}},
        {'type': 'prop-update', 'value': {'_isnumeral': 'yes', POSPEECH: ADVERB}, 'endow': {'derivative': NUMERAL, 'class': 'cardinal'}},
        {'type': 'prop-update', 'value': {'_isnumeral': 'yes', POSPEECH: VERB}, 'endow': {'derivative': NUMERAL, 'class': 'cardinal'}},
        {'type': 'prop-update', 'value': {'_isnumeral': 'yes', POSPEECH: NOUN}, 'endow': {'derivative': NUMERAL, 'class': 'cardinal'}},
        {'type': 'prop-delete', 'value': {'_isnumeral': 'yes'}, 'endow': ['_isnumeral']},
        {'type': 'prop-update', 'value': {'notword': 'figure'}, 'endow': {POSPEECH: NUMERAL, 'class': 'cardinal'}},
        {'type': 'prop-function', 'value': {'notword': 'figure'}, 'endow': convert_figure},
    ],
]


def set_properties_by_signs(word, signs):
    def has_all_properties(dict1, dict2):
        for k, v in dict2.items():
            if dict1.get(k) != v:
                return False

        return True

    def check_word(word, type_sign: str, value):
        if type_sign == 'prop':
            return has_all_properties(word, value)
        elif type_sign == 'end' and word['base'].endswith(value):
            word['base'] = word['base'][:-len(value)]
            return True
        elif type_sign == 'prefix' and word['word'].startswith(value):
            word['base'] = word['base'][len(value):]
            return True
        elif type_sign == 'case_of_first_letter':
            first_letter = word['word'][:1]
            return (first_letter.islower() and value == 'lower') or (first_letter.isupper() and value == 'upper')
        elif type_sign == 'word' and value == word['word_lower']:
            return True
        elif type_sign == 'function':
            return value(word)

    def do_endow(word, type_endow, endow):
        if type_endow == 'update':
            word.update(endow)
        elif type_endow == 'default':
            for k, v in endow.items():
                if k not in word:  # word.setdefault(k, v)
                    word[k] = v
        elif type_endow == 'delete':
            for key in endow:
                del word[key]
        elif type_endow == 'function':
            return endow(word)

    word['base'] = word['word'].lower()
    word['word_lower'] = word['word'].lower()
    for layer in signs:
        for sign in layer:
            need_continue = False
            for ifnot in sign.get('if-not', []):
                if has_all_properties(word, ifnot):
                    need_continue = True
                    break

            if need_continue:
                continue

            if '-' not in sign['type']:
                sign['type'] = '{}-update'.format(sign['type'])

            type_sign, type_endow = sign['type'].split('-')
            if check_word(word, type_sign, sign['value']) and sign.get('endow'):
                do_endow(word, type_endow, sign['endow'])


def analyze(message):
    for sentence in message.text:
        for word in sentence:
            set_properties_by_signs(word, signs)

    return message.text
