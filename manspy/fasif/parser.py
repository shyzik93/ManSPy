import os
import json
import inspect

from manspy.relation import ObjRelation
from manspy.fasif import finder
from manspy.message import Message
from manspy.analyse_text import nature2internal
from manspy.utils import importer


def get_is_required(func):
    if not func.__code__.co_argcount:
        raise Exception('The function must have 1 or more arguments')

    first_arg_name = func.__code__.co_varnames[0]
    signature = inspect.signature(func)
    is_required = {}
    for k, v in signature.parameters.items():
        if k == first_arg_name:
            continue

        is_required[k] = v.default is inspect.Parameter.empty

    return is_required


def get_dword(word, settings):
    levels = settings.levels
    settings.levels = ':postmorph'
    message = Message(settings, word)
    text = nature2internal(message)
    settings.levels = levels
    return list(text(0).getUnit('dict').values())[0]


def process_verb(fasif, OR, settings, path_import):
    fasif['function'] = os.path.join(path_import, fasif['function'])
    for language, verbs in fasif['verbs'].items():
        if language in settings.modules['language']:
            words = [get_dword(word_verb, settings)['base'] for word_verb in verbs]
            id_group = OR.setRelation('synonym', *words)
            fasif['verbs'][language] = id_group

    return fasif


def process_word_combination(fasif, OR, settings, path_import):
    not_to_db = ['nombr', 'cifer']

    get_condition = fasif['functions'].get('getCondition')
    get_condition_is_required = None
    if get_condition:
        get_condition['function'] = os.path.join(path_import, get_condition['function'])
        function = importer.action(get_condition['function'])
        get_condition_is_required = get_is_required(function)

    change_condition = fasif['functions'].get('changeCondition')
    change_condition_is_required = None
    if change_condition:
        change_condition['function'] = os.path.join(path_import, change_condition['function'])
        function = importer.action(change_condition['function'])
        change_condition_is_required = get_is_required(function)

    if None not in (get_condition_is_required, change_condition_is_required):
        if get_condition_is_required != change_condition_is_required:
            raise Exception('arguments for `get_condition` and `change_condition` must be equals')

    is_required = get_condition_is_required or change_condition_is_required

    fasif['argdescr'] = {}
    for language in settings.modules['language']:
        for arg_name, args in fasif['args'].items():
            argtables = args['argtable'].setdefault(language, {})
            for arg_word, argtable in argtables.copy().items():
                del argtables[arg_word]
                arg_word = get_dword(arg_word, settings)['base']
                argtables[arg_word] = argtable

            argwords = args['argwords'][language]
            argwords['name'] = get_dword(argwords['name'], settings)
            for index, argword in enumerate(argwords['hyperonyms']):
                argwords['hyperonyms'][index] = get_dword(argword, settings)

        for destination, value in fasif['functions'].items():
            verbs = value['verbs'].setdefault(language, {})
            for index, word_verb in enumerate(verbs):
                verbs[index] = OR.setRelation('synonym', get_dword(word_verb, settings)['base'])

        levels = settings.levels
        settings.levels = ':synt'
        message = Message(settings, fasif['wcomb'][language])
        wcomb = nature2internal(message)(0)
        settings.levels = levels
        fasif['argdescr'][language] = {}
        for argname, data in fasif['args'].items():
            argword = data['argwords'][language]['name']
            wcomb.chmanyByValues(
                {'argname': argname},
                setstring='subiv:noignore',
                base=argword.get('base'),
                case=argword.get('case')
            )
            fasif['argdescr'][language][argname] = {
                'isreq': is_required[argname],
                'argtable': data['argtable'][language],
                'hyperonyms': data['argwords'][language]['hyperonyms']
            }

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
                    fasif = fasif_processor(fasif, OR, settings, path_import)
                    if fasif:
                        fdb.safe(fasif["type"], fasif)
