# -*- coding: utf-8 -*-
''' Модуль выполняет стандартный морфологический анализ слова ЕЯ Эсперанто,
    основывваясь только на морфологических признаках (на внешнем виде слова)
'''

from . import Dict
import re

combain_numerals_template = re.compile(
        '^({})({}|{})$'.format(
            '|'.join(Dict.dct['numeral'][:-5]),
            Dict.dct['numeral'][-5],
            Dict.dct['numeral'][-4],
        )
)
mili_numerals_template = re.compile(('^(%s)(iliard|ilion)$') % '|'.join(Dict.dct['numeral'][:-5]))


def set_properties_by_signs(word, signs):
    word['base'] = word['word'].lower()
    word['word_lower'] = word['word'].lower()
    for layer in signs:
        for sign in layer:
            if sign['type'] == 'end' and word['base'].endswith(sign['value']):
                word.update(sign['endow'])
                word['base'] = word['base'][:-len(sign['value'])]

            elif sign['type'] == 'prefix' and word['word'].startswith(sign['value']):
                word.update(sign['endow'])
                word['base'] = word['base'][len(sign['value']):]

            elif sign['type'] == 'case_of_first_letter':
                first_letter = word['word'][:1]
                if first_letter.islower() and sign['value'] == 'lower':
                    word.update(sign['endow'])

                if first_letter.isupper() and sign['value'] == 'upper':
                    word.update(sign['endow'])

            elif sign['type'] == 'word' and sign['value'] == word['word_lower']:
                word.update(sign['endow'])

            elif sign['type'] == 'prop-default':
                has_all_properties = True
                for k, v in sign['value'].items():
                    if word.get(k) != v:
                        has_all_properties = False
                        break

                if has_all_properties:
                    for k, v in sign['endow'].items():
                        if k not in word:
                            word[k] = v

            elif sign['type'] == 'prop':
                has_all_properties = True
                for k, v in sign['value'].items():
                    if word.get(k) != v:
                        has_all_properties = False
                        break

                if has_all_properties:
                    word.update(sign['endow'])


def checkByDict(word_l, word):
    ''' Определяет часть речи по словарю
        для неизменяемых или почти неизменяемых частей речи'''
    for POSpeech, data in Dict.words.items():
        if word_l not in data:
            continue

        word.update(data[word_l])
        word['POSpeech'] = POSpeech
        word['base'] = word_l
        return True


def is_numeral(word):
    """ word_l - корень числительного, word - одно слово """
    word_l = word['base']
    if word_l in Dict.words['numeral']:
        word.update(Dict.words['numeral'][word_l])
        return True

    combain_numerals = combain_numerals_template.findall(word_l)
    if combain_numerals:
        combain_numerals = combain_numerals[0]

    mili_numerals = mili_numerals_template.findall(word_l)
    if mili_numerals:
        mili_numerals = mili_numerals[0]

    if combain_numerals:
        factor1, factor2 = combain_numerals
        number_value = int(Dict.dct['numeral_d'][factor2]) * int(Dict.dct['numeral_d'][factor1])
    elif mili_numerals:
        factor1, factor2 = mili_numerals
        number_value = int(Dict.dct['numeral_d']['milion']) ** int(Dict.dct['numeral_d'][factor1])
        if factor2 == 'iliard':
            number_value *= 1000
    else:
        return False

    word['number_value'] = number_value
    return True


def _getMorphA(word):
    # Определение части речи по словарю
    # (для неизменяемых или почти неизменяемых частей речи)
    if checkByDict(word['word'].lower(), word):
        return

    #combain_numerals = combain_numerals_template.findall(word_l)
    #if combain_numerals: combain_numerals = combain_numerals[0]
    #mili_numerals = mili_numerals_template.findall(word_l)
    #if mili_numerals: mili_numerals = mili_numerals[0]
    #print combain_numerals, mili_numerals

    set_properties_by_signs(word, Dict.signs)

    # наречие, глагол и существительное
    if word.get('POSpeech') in ('adverb', 'verb', 'noun'):
        if is_numeral(word):
            word['derivative'] = 'numeral'  # производное от числительного

    # прилагательное, притяжательное местоимение или порядковое числительное
    elif word.get('POSpeech') == 'adjective':
        if checkByDict(word['base'], word):  # прилагательное
            if word['POSpeech'] == 'numeral':  # порядковое числительное
                word['class'] = 'ordinal'
            else:  # прилагательное (есть ли такие: dea, laa, kaja и подобные?)
                word['POSpeech'] = 'adjective'
                word['case'] = 'nominative'
                word['number'] = 'singular'
        elif is_numeral(word):  # порядковое числительное
            word['POSpeech'] = 'numeral'
            word['class'] = 'ordinal'

    # мн. ч. существительно, прилагательного, притяжательно местоимения. И вин. падеж прилагательного, существительного, местоимения или притяхательного местоимения.
    #ERROR слово prezenten и enden определяется наречием. Другие слова на -n могут ошибочно определиться.

    # сложное числительное (не составные!)
    elif is_numeral(word):#combain_numerals:#len_word >= 5:
        #factor1, factor2 = combain_numerals
        word['POSpeech'] = 'numeral'
        word['class'] = 'cardinal' # количественное
        #word['number_value'] = int(Dict.dct['numeral_d'][factor1]) * int(Dict.dct['numeral_d'][factor2])

    # число (считается как числительное)
    elif word['notword'] == 'figure':#re.match(r'[0-9]+(\.|\,)?[0-9]*', word_l):
        word['POSpeech'] = 'numeral'
        word['class'] = 'cardinal'
        word['number_value'] = float(word['word_lower'].replace(',', '.'))


def get_analysis(text):
    ''' Обёртка '''
    for sentence in text:
        for word in sentence:
            _getMorphA(word)
    return text

#sentence = 'vi montru kursojn de mia dolaro'
#sentence = '1444 123.78654 345,976 0.7 9,8'
#sentence = 'triA unu Tridek kvarcent du mil'
