import re
import os

from manspy.fasif.parser_fasif import FASIF
from manspy.fasif.constants import *
from manspy.message import Message
from manspy.analyse_text import nature2internal


class FASIF_WordCombination(FASIF):

    def parse(self, _fasif, path_import):
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
        lang = None

        arg_indexes = []
        arg_index = 0

        for string in _fasif:
            ## Блок функций
            # Назначение: Модуль/Функция
            if re.findall(STRING_DESTINATION_TITLE, string): # "Name_01 : moduleName/funcName "
                destination, function = string.split(':')
                functions[destination.strip()] = {'function': os.path.join(path_import, function.strip()), 'verbs': {}}
                #print '1 $$$$', string
            # Язык: глаголДляФункции
            elif re.findall(STRING_DESTINATION_BODY, string): # "    Language : verbглагол"
                lang, verb = string.split(':')
                functions[destination]['verbs'][lang.strip().lower()] = verb.strip().split()
                #print '2 $$$$', string
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
                for lang in string:
                    args[arg_name]['argtable'][lang.strip().lower()] = {}
                    lang_indexes.append(lang.strip().lower())

                arg_indexes.append(arg_name)
                #print '3 $$$$', string
            elif re.findall(STRING_ARGUMENT_TITLE2, string):
                arg_name, isreq = string.split()
                args_as_list = False

                if len(isreq) == 2:
                    args_as_list = isreq[1]
                    isreq = isreq[0]

                args[arg_name] = {'isreq': isreq, 'args_as_list': args_as_list, 'argtable': {}, 'argwords': {}}
                arg_indexes.append(arg_name)
                #print '3 $$$$', string
            # Аргумент ; АргументноеСловоНаЯзыке1 ; АргументноеСловоНаЯзыке2
            elif re.findall(STRING_ARGUMENT_BODY, string):
                string = string.strip().split(';')
                arg_value = string.pop(0).strip()
                for index, word in enumerate(string):
                    word = word.strip()
                    if not word: continue
                    args[arg_name]['argtable'][lang_indexes[index]][word] = arg_value
                #print '4 $$$$', string
            elif re.findall(STRING_ARGUMENT_TITLE2, string):
                arg_name, isreq = string.split()
                args[arg_name] = {'isreq': isreq, 'argtable': {}, 'argwords': {}}
                arg_indexes.append(arg_name)
            ## Блок словосочетаний
            # Язык
            elif re.findall(STRING_WCOMB_TITLE, string):
                lang = string.strip().lower()
                for arg_name in args:
                    args[arg_name]['argwords'][lang] = {'in_wcomb': {'name': None, 'hyperonyms': []}, 'another': []}
                arg_index = 0
                #print '5 $$$$', string
            # АргументноеСлово: АбстрактнаяГруппа1, АбстрактнаяГруппа2     Необходимо заменитиь на: # АргументноеСлово: ВходитАбстрГруппа1, ВходитАбстрГруппа2; НеВХодитАбстрГрупп, НеВХодитАбстрГрупп
            elif re.findall(STRING_WCOMB_ARGWORD, string):
                arg_words = string.strip().split(';')
                #print arg_index, string
                arg_word, hyperonyms = arg_words.pop(0).split(':')
                args[arg_indexes[arg_index]]['argwords'][lang]['in_wcomb']['name'] = arg_word
                for hyperonym in hyperonyms.split(','):
                    args[arg_indexes[arg_index]]['argwords'][lang]['in_wcomb']['hyperonyms'].append(hyperonym.strip())

                for _arg_word in arg_words:
                    arg_word, hyperonyms = _arg_word.split(':')
                    args[arg_indexes[arg_index]]['argwords'][lang]['another']['name'] = arg_word
                    for hyperonym in hyperonyms.split(','):
                        args[arg_indexes[arg_index]]['argwords'][lang]['another']['hyperonyms'].append(hyperonym.strip())
                arg_index += 1
                #print '6 $$$$', string
            elif re.findall(STRING_WCOMB, string):
                  wcomb[lang.lower()] = string.strip()
        return {'functions': functions, 'wcomb': wcomb, 'args': args}

    def siftout(self, fasif, lang):
        args = {}
        for arg_name, _args in fasif['args'].items():
            argtable = _args['argtable']
            if lang in argtable:
                _args['argtable'] = argtable[lang]
            elif not argtable:
                _args['argtable'] = {}
            else:
                return None
            argwords = _args['argwords']
            if lang in argwords:
                _args['argwords'] = argwords[lang]
            else:
                return None

        for destination, value in fasif['functions'].items():
            if lang in value['verbs']:
                value['verbs'] = value['verbs'][lang]
            else:
                value['verbs'] = []

        if lang in fasif['wcomb']:
            fasif['wcomb'] = fasif['wcomb'][lang]
        else:
            return None

        return fasif

    def proccess_lingvo_data(self, fasif, OR, fdb, settings):
        for arg_name, data in fasif['args'].items():
            _data = data['argtable'].copy().items()
            for arg_word, argtable in _data:
                del data['argtable'][arg_word]
                arg_word = self.get_dword(arg_word, settings)['base']
                data['argtable'][arg_word] = argtable

            self.proccess_argword(data['argwords']['in_wcomb'], settings)
            for argword in data['argwords']['another']:
                self.proccess_argword(argword, settings)

        for destination, value in fasif['functions'].items():
            for index, word_verb in enumerate(value['verbs']):
                value['verbs'][index] = OR.setRelation('synonym', self.get_dword(word_verb, settings)['base'])

        #print '----------------- to formule start'
        message = Message(settings, {'levels':':synt', 'print_time':False}, fasif['wcomb'], 'W')
        wcomb = nature2internal(message)(0)
        fasif['argdescr'] = {}
        for argname, data in fasif['args'].items():
            argword = data['argwords']['in_wcomb']['name']
            wcomb.chmanyByValues({'argname':argname}, setstring='subiv:noignore', base=argword['base'], case=argword['case'])
            fasif['argdescr'][argname] = {
                'isreq': data['isreq'],
                'argtable': data['argtable'],
                'argwords_another': data['argwords']['another'],
                'hyperonyms': data['argwords']['in_wcomb']['hyperonyms']
            }
            if len(fasif['args']) == 1:  # а при числе аргументов более 1 мы их передаём только как именованные
                fasif['args_as_list'] = data['args_as_list']
            else:
                fasif['args_as_list'] = False
        del fasif['args']

        fasif['wcomb'] = wcomb.getUnit('dict')
        for argname, data in fasif['argdescr'].items():
            data['isreq'] = True if data['isreq'] == 'y' else False
            for hyperonym in data['hyperonyms']:
                argword = [argword for argword in wcomb.getByValues(setstring='subiv:noignore', argname=argname)][0]
                #print argname, argword
                if argword[1]:
                    base = argword[1]['base']
                else:
                    base = argword[2][0]['base']
                bases = data['argtable'].keys()
                if hyperonym['base'] not in not_to_db:
                    OR.setRelation('hyperonym', hyperonym['base'], base, *bases)

        #pprint(fasif['args'])
        #fwcomb = to_formule.to_formule(fasif['wcomb'], True, fasif['args'])
        #pprint(fwcomb)
        #fdb.add_hashWComb(fwcomb, {'bl':4}, sentence.getUnit('str')['fwords'], '')

        #print '----------------- to formule end'

        return fasif