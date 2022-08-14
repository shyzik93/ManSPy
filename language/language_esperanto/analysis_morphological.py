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

            elif sign['type'] == 'function':
                sign['value'](word)
                if sign['endow']:
                    word.update(sign['endow'])


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


