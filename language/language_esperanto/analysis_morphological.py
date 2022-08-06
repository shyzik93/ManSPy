# -*- coding: utf-8 -*-
''' Модуль выполняет стандартный морфологический анализ слова ЕЯ Эсперанто,
    основывваясь только на морфологических признаках (на внешнем виде слова)
'''

from . import Dict
import re

#template = re.compile(r'[0-9]+(\.|\,)?[0-9]*')

combain_numerals_template = re.compile(('^(%s)(' + Dict.dct['numeral'][-5] + '|' + Dict.dct['numeral'][-4] + ')$') % '|'.join(
    Dict.dct['numeral'][:-5]
))
mili_numerals_template = re.compile(('^(%s)(iliard|ilion)$') % '|'.join(Dict.dct['numeral'][:-5]))


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


def getNumberAndCase(word_l):
    '''возвращает число, падеж и начальную форму
       (функция для прилагательного, существительного или местоимения)'''
    temp_word = {'case': 'nominative',
           'number': 'singular' }
    if word_l[-1] == 'n':
        word_l = word_l[:-1]
        temp_word['case'] = 'accusative'
    if word_l[-1] == 'j':
        word_l = word_l[:-1]
        temp_word['number'] = 'plural'
    temp_word['base'] = word_l
    return temp_word


def defaultNoun(word_l, word):
    ''' Устанавливает параметры по умолчанию
        На вход подаётся слово без окончания'''
    word['case'] = 'nominative' # именительный
    # определение по первой букве:
    if not word['word'][0].islower():
        word['name'] = 'proper'  # имя собственное
    else:
        word['name'] = 'common'  # имя нарицательное


def is_numeral(word_l, word):
    """ word_l - корень числительного, word - одно слово """
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
    word_l = word['word'].lower()
    # Определение части речи по словарю
    # (для неизменяемых или почти неизменяемых частей речи)
    if checkByDict(word_l, word):
        return

    #combain_numerals = combain_numerals_template.findall(word_l)
    #if combain_numerals: combain_numerals = combain_numerals[0]
    #mili_numerals = mili_numerals_template.findall(word_l)
    #if mili_numerals: mili_numerals = mili_numerals[0]
    #print combain_numerals, mili_numerals

    word['base'] = word['word'].lower()
    for sign in Dict.signs:
        if sign['type'] == 'end' and word['word'].endswith(sign['value']):
            word.update(sign['endow'])
            word['base'] = word['base'][:-len(sign['value'])]
        elif sign['type'] == 'prefix' and word['word'].startswith(sign['value']):
            word.update(sign['endow'])
            word['base'] = word['base'][len(sign['value']):]

    # наречие, глагол и существительное
    if word.get('POSpeech') in ('adverb', 'verb', 'noun'):
        if word.get('POSpeech') == 'noun':
            defaultNoun(word['base'], word)

        if is_numeral(word['base'], word):
            word['derivative'] = 'numeral'  # производное от числительного

    # прилагательное, притяжательное местоимение или порядковое числительное
    elif word.get('POSpeech') == 'adjective':
        if checkByDict(word['base'], word):  # прилагательное
            if word['POSpeech'] == 'pronoun':  # притяжательное иестоимение
                word['category'] = 'possessive'
            elif word['POSpeech'] == 'numeral':  # порядковое числительное
                word['class'] = 'ordinal'
            else:  # прилагательное (есть ли такие: dea, laa, kaja и подобные?)
                word['POSpeech'] = 'adjective'
                word['case'] = 'nominative'
                word['number'] = 'singular'
        elif is_numeral(word['base'], word):  # порядковое числительное
            word['POSpeech'] = 'numeral'
            word['class'] = 'ordinal'
        else:
            word['POSpeech'] = 'adjective'
            word['case'] = 'nominative'
            word['number'] = 'singular'

    # мн. ч. существительно, прилагательного, притяжательно местоимения. И вин. падеж прилагательного, существительного, местоимения или притяхательного местоимения.
    #ERROR слово prezenten и enden определяется наречием. Другие слова на -n могут ошибочно определиться.
    elif word_l.endswith('j') or word_l.endswith('n') or word_l.endswith('jn'):
        temp_word1 = getNumberAndCase(word_l)
        temp_word2 = {'word': temp_word1['base']}
        _getMorphA(temp_word2)
        word.update(temp_word2)
        word.update(temp_word1)
        word['word'] = word_l
        word['base'] = temp_word2['base']

    # сложное числительное (не составные!)
    elif is_numeral(word_l, word):#combain_numerals:#len_word >= 5:
        #factor1, factor2 = combain_numerals
        word['POSpeech'] = 'numeral'
        word['word'] = word_l
        word['base'] = word_l
        word['class'] = 'cardinal' # количественное
        #word['number_value'] = int(Dict.dct['numeral_d'][factor1]) * int(Dict.dct['numeral_d'][factor2])

    # число (считается как числительное)
    elif word['notword'] == 'figure':#re.match(r'[0-9]+(\.|\,)?[0-9]*', word_l):
        word['POSpeech'] = 'numeral'
        word['class'] = 'cardinal'
        word['word'] = word_l
        word['base'] = word_l
        word['number_value'] = float(word_l.replace(',', '.'))

    if not word.get('POSpeech'):
        # нераспознанное слово с большой буквы - существительное
        if not word['word'][0].islower():
            defaultNoun(word_l, word)


def get_analysis(text):
    ''' Обёртка '''
    for sentence in text:
        for word in sentence:
            _getMorphA(word)
    return text

#sentence = 'vi montru kursojn de mia dolaro'
#sentence = '1444 123.78654 345,976 0.7 9,8'
#sentence = 'triA unu Tridek kvarcent du mil'
