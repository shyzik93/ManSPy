import re
import os

from manspy.fasif.parser_fasif import FASIF
from manspy.fasif.constants import *
from manspy.message import Message
from manspy.analyse_text import nature2internal


class FASIF_WordCombination(FASIF):

    def parse(self, _fasif, path_import, settings):
        """
            подформат состоит из трёх блоков: описание функций, аргументов и словосочетания.
            Аргументы одинаковы для всех функций
        """
        functions = {}
        args = {}
        wcomb = {}

        ## Блок функций
        destination = None
        ## Блок аргументов
        arg_name = None
        lang_indexes = []
        ## Блок словосочетаний
        language = None

        arg_indexes = []
        arg_index = 0

        for string in _fasif:
            ## Блок функций
            # Назначение: Модуль/Функция
            if re.findall(STRING_DESTINATION_TITLE, string):  # "Name_01 : moduleName/funcName "
                destination, function = string.split(':')
                functions[destination.strip()] = {'function': os.path.join(path_import, function.strip()), 'verbs': {}}
            # Язык: глаголДляФункции
            elif re.findall(STRING_DESTINATION_BODY, string): # "    Language : verbглагол"
                language, verb = string.split(':')
                language = language.strip().lower()
                if language in settings.modules['language']:
                    functions[destination]['verbs'][language] = verb.strip().split()
            ## Блок аргументов
            # аргумент yORn ; Язык1 ; Язык2
            elif re.findall(STRING_ARGUMENT_TITLE1, string):
                string = string.split(';')
                arg_name, isreq = string.pop(0).split()
                args_as_list = False

                if len(isreq) == 2:
                    args_as_list = isreq[1]
                    isreq = isreq[0]

                lang_indexes = []
                args[arg_name] = {'isreq': isreq, 'args_as_list': args_as_list, 'argtable': {}, 'argwords': {}}
                for language in string:
                    language = language.strip().lower()
                    if language in settings.modules['language']:
                        args[arg_name]['argtable'][language] = {}
                    lang_indexes.append(language)

                arg_indexes.append(arg_name)
            elif re.findall(STRING_ARGUMENT_TITLE2, string):
                arg_name, isreq = string.split()
                args_as_list = False

                if len(isreq) == 2:
                    args_as_list = isreq[1]
                    isreq = isreq[0]

                args[arg_name] = {'isreq': isreq, 'args_as_list': args_as_list, 'argtable': {}, 'argwords': {}}
                arg_indexes.append(arg_name)
            # Аргумент ; АргументноеСловоНаЯзыке1 ; АргументноеСловоНаЯзыке2
            elif re.findall(STRING_ARGUMENT_BODY, string):
                string = string.strip().split(';')
                arg_value = string.pop(0).strip()
                for index, word in enumerate(string):
                    word = word.strip()
                    language = lang_indexes[index]
                    if language in settings.modules['language'] and word:
                        args[arg_name]['argtable'][language][word] = arg_value
            elif re.findall(STRING_ARGUMENT_TITLE2, string):
                arg_name, isreq = string.split()
                args[arg_name] = {'isreq': isreq, 'argtable': {}, 'argwords': {}}
                arg_indexes.append(arg_name)
            ## Блок словосочетаний
            # Язык
            elif re.findall(STRING_WCOMB_TITLE, string):
                language = string.strip().lower()
                if language in settings.modules['language']:
                    for arg_name in args:
                        args[arg_name]['argwords'][language] = {'in_wcomb': {'name': None, 'hyperonyms': []}, 'another': []}
                arg_index = 0
            # АргументноеСлово: АбстрактнаяГруппа1, АбстрактнаяГруппа2     Необходимо заменитиь на: # АргументноеСлово: ВходитАбстрГруппа1, ВходитАбстрГруппа2; НеВХодитАбстрГрупп, НеВХодитАбстрГрупп
            elif re.findall(STRING_WCOMB_ARGWORD, string):
                if language in settings.modules['language']:
                    arg_words = string.strip().split(';')
                    arg_word, hyperonyms = arg_words.pop(0).split(':')
                    args[arg_indexes[arg_index]]['argwords'][language]['in_wcomb']['name'] = arg_word
                    for hyperonym in hyperonyms.split(','):
                        args[arg_indexes[arg_index]]['argwords'][language]['in_wcomb']['hyperonyms'].append(hyperonym.strip())

                    for _arg_word in arg_words:
                        arg_word, hyperonyms = _arg_word.split(':')
                        args[arg_indexes[arg_index]]['argwords'][language]['another']['name'] = arg_word
                        for hyperonym in hyperonyms.split(','):
                            args[arg_indexes[arg_index]]['argwords'][language]['another']['hyperonyms'].append(hyperonym.strip())
                arg_index += 1
            elif re.findall(STRING_WCOMB, string):
                if language in settings.modules['language']:
                    wcomb[language.lower()] = string.strip()

        return {'functions': functions, 'wcomb': wcomb, 'args': args}

    def proccess_lingvo_data(self, fasif, OR, fdb, settings):
        fasif['argdescr'] = {}
        for language in settings.modules['language']:
            for arg_name, data in fasif['args'].items():
                _data = data['argtable'].setdefault(language, {}).copy().items()
                for arg_word, argtable in _data:
                    del data['argtable'][language][arg_word]
                    arg_word = self.get_dword(arg_word, settings)['base']
                    data['argtable'][language][arg_word] = argtable

                self.proccess_argword(data['argwords'][language]['in_wcomb'], settings)
                for argword in data['argwords'][language]['another']:
                    self.proccess_argword(argword, settings)

            for destination, value in fasif['functions'].items():
                verbs = value['verbs'].setdefault(language, {})
                for index, word_verb in enumerate(verbs):
                    verbs[index] = OR.setRelation('synonym', self.get_dword(word_verb, settings)['base'])

            #print '----------------- to formule start'
            levels = settings.levels
            settings.levels = ':synt'
            message = Message(settings, {}, fasif['wcomb'][language], 'W')
            wcomb = nature2internal(message)(0)
            settings.levels = levels
            fasif['argdescr'][language] = {}
            for argname, data in fasif['args'].items():
                argword = data['argwords'][language]['in_wcomb']['name']
                wcomb.chmanyByValues({'argname':argname}, setstring='subiv:noignore', base=argword.get('base'), case=argword.get('case'))
                fasif['argdescr'][language][argname] = {
                    'isreq': data['isreq'],
                    'argtable': data['argtable'][language],
                    'argwords_another': data['argwords'][language]['another'],
                    'hyperonyms': data['argwords'][language]['in_wcomb']['hyperonyms']
                }
                if len(fasif['args']) == 1:  # а при числе аргументов более 1 мы их передаём только как именованные
                    fasif['args_as_list'] = data['args_as_list']
                else:
                    fasif['args_as_list'] = False
            del fasif['args']

            fasif['wcomb'][language] = wcomb.getUnit('dict')
            for argname, data in fasif['argdescr'][language].items():
                data['isreq'] = True if data['isreq'] == 'y' else False
                for hyperonym in data['hyperonyms']:
                    argword = [argword for argword in wcomb.getByValues(setstring='subiv:noignore', argname=argname)][0]
                    if argword[1]:
                        base = argword[1]['base']
                    else:
                        base = argword[2][0]['base']
                    bases = data['argtable'].keys()
                    if hyperonym['base'] not in not_to_db:
                        OR.setRelation('hyperonym', hyperonym['base'], base, *bases)

        return fasif