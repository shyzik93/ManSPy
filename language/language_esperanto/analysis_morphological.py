# -*- coding: utf-8 -*-
''' Модуль выполняет стандартный морфологический анализ слова ЕЯ Эсперанто,
    основывваясь только на морфологических признаках (на внешнем виде слова)
'''

from . import Dict
import re

combain_numerals_template = re.compile(
        '^({})({}|{})$'.format(
            '|'.join(Dict.numeral_list[:-5]),
            Dict.numeral_list[-5],
            Dict.numeral_list[-4],
        )
)
mili_numerals_template = re.compile('^({})(iliard|ilion)$'.format('|'.join(Dict.numeral_list[:-5])))


def set_properties_by_signs(word, signs):
    def has_all_properties(dict1, dict2):
        for k, v in dict2.items():
            if dict1.get(k) != v:
                return False

        return True

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
                if has_all_properties(word, sign['value']):
                    for k, v in sign['endow'].items():
                        if k not in word:
                            word[k] = v

            elif sign['type'] == 'prop':
                if has_all_properties(word, sign['value']):
                    word.update(sign['endow'])


def is_numeral(word):
    word_l = word['base']
    if word_l in Dict.words['numeral']:
        word.update(Dict.words['numeral'][word_l])
        return True

    combain_numerals = combain_numerals_template.findall(word_l)
    if combain_numerals:
        factor1, factor2 = combain_numerals[0]
        word['number_value'] = int(Dict.numeral_dict[factor2]) * int(Dict.numeral_dict[factor1])

    mili_numerals = mili_numerals_template.findall(word_l)
    if mili_numerals:
        factor1, factor2 = mili_numerals[0]
        word['number_value'] = int(Dict.numeral_dict['milion']) ** int(Dict.numeral_dict[factor1])
        if factor2 == 'iliard':
            word['number_value'] *= 1000

    return bool(combain_numerals) or bool(mili_numerals)


def _getMorphA(word):
    set_properties_by_signs(word, Dict.signs)

    # наречие, глагол и существительное
    if word.get('POSpeech') in ('adverb', 'verb', 'noun') and is_numeral(word):
        word['derivative'] = 'numeral'  # производное от числительного

    # прилагательное, притяжательное местоимение или порядковое числительное
    elif word.get('POSpeech') == 'adjective' and is_numeral(word):
        word['number_value'] = Dict.words['numeral'][word['base']]['number_value']
        word['POSpeech'] = 'numeral'
        word['class'] = 'ordinal'

    # сложное числительное (не составные!)
    elif is_numeral(word):
        word['POSpeech'] = 'numeral'
        word['class'] = 'cardinal'  # количественное

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
