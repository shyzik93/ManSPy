# -*- coding: utf-8 -*-
''' Модуль выполняет стандартный морфологический анализ слова ЕЯ Эсперанто,
    основывваясь только на морфологических признаках (на внешнем виде слова)
'''

from . import Dict


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


def get_analysis(text):
    ''' Обёртка '''
    for sentence in text:
        for word in sentence:
            set_properties_by_signs(word, Dict.signs)
            if word['notword'] == 'figure':
                word['POSpeech'] = 'numeral'
                word['class'] = 'cardinal'
                word['number_value'] = float(word['word_lower'].replace(',', '.'))
    return text


