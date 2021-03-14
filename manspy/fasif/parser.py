import os
import json

from manspy.relation import ObjRelation
from manspy.fasif import finder
from manspy.message import Message
from manspy.analyse_text import nature2internal


def get_dword(word, settings):
    levels = settings.levels
    settings.levels = ':postmorph'
    message = Message(settings, {}, word, 'W')
    text = nature2internal(message)
    settings.levels = levels
    return list(text(0).getUnit('dict').values())[0]


def proccess_argword(argwords, settings):
    argwords['name'] = get_dword(argwords['name'], settings)
    for index, argword in enumerate(argwords['hyperonyms']):
        argwords['hyperonyms'][index] = get_dword(argword, settings)


def process_verb(fasif, OR, fdb, settings, path_import):
    fasif['function'] = os.path.join(path_import, fasif['function'])
    for language, verbs in fasif['verbs'].items():
        if language in settings.modules['language']:
            words = [get_dword(word_verb, settings)['base'] for word_verb in verbs]
            id_group = OR.setRelation('synonym',
                                      *words)  # функция должна возвратить группу, если добавлен хотя бы один синоним
            fasif['verbs'][
                language] = id_group  # TODO: если идентификатор группы отсутсвует (None), то фасиф считается недействительным и не добавляется в базу (игнорируется)
        else:
            fasif['verbs'][language] = None
    return fasif


def process_word_combination(fasif, OR, fdb, settings, path_import):
    not_to_db = ['nombr', 'cifer']
    get_condition = fasif['functions'].get('getCondition')
    if get_condition:
        get_condition['function'] = os.path.join(path_import, get_condition['function'])

    change_condition = fasif['functions'].get('changeCondition')
    if change_condition:
        change_condition['function'] = os.path.join(path_import, change_condition['function'])

    fasif['argdescr'] = {}
    for language in settings.modules['language']:
        for arg_name, data in fasif['args'].items():
            _data = data['argtable'].setdefault(language, {}).copy().items()
            for arg_word, argtable in _data:
                del data['argtable'][language][arg_word]
                arg_word = get_dword(arg_word, settings)['base']
                data['argtable'][language][arg_word] = argtable

            proccess_argword(data['argwords'][language]['in_wcomb'], settings)

        for destination, value in fasif['functions'].items():
            verbs = value['verbs'].setdefault(language, {})
            for index, word_verb in enumerate(verbs):
                verbs[index] = OR.setRelation('synonym', get_dword(word_verb, settings)['base'])

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
                'hyperonyms': data['argwords'][language]['in_wcomb']['hyperonyms']
            }
            if len(fasif['args']) == 1:  # а при числе аргументов более 1 мы их передаём только как именованные
                fasif['args_as_list'] = data['args_as_list']
            else:
                fasif['args_as_list'] = False
        del fasif['args']

        fasif['wcomb'][language] = wcomb.getUnit('dict')
        for argname, data in fasif['argdescr'][language].items():
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


def fasif_parser(path_import, settings):
    OR = ObjRelation(settings.c, settings.cu)
    fdb = finder.FasifDB(settings.c, settings.cu)

    for fasif_file_name in os.listdir(path_import):
        if fasif_file_name.endswith('.json'):
            with open(os.path.join(path_import, fasif_file_name), encoding='utf-8') as fasif_file:
                fasifs = json.load(fasif_file)
                for fasif in fasifs:
                    fasif_processor = 'process_{}'.format(fasif["type"])
                    fasif_processor = globals()[fasif_processor]
                    fasif = fasif_processor(fasif, OR, fdb, settings, path_import)
                    if fasif:
                        fdb.safe(fasif["type"], fasif)
