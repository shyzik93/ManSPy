import os
import json
import inspect

from manspy.analyzers import (
    esperanto_morphological,
    esperanto_syntax,
    esperanto_graphemathic,
    esperanto_postmorphological,
)
from manspy.relation import Relation
from manspy.message import Message
from manspy.analyse_text import nature2internal
from manspy.utils import importer

analyzers = [esperanto_graphemathic, esperanto_morphological, esperanto_postmorphological, esperanto_syntax]


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
    message = Message(settings, word)
    text = nature2internal(message, analyzers=analyzers[:-1])
    return text(0).getByPos(0)


def process_verb(fasif, obj_relation, settings, path_import):
    fasif['function'] = os.path.join(path_import, fasif['function'])
    for language, verbs in fasif['verbs'].items():
        if language in settings.languages:
            words = [get_dword(word_verb, settings) for word_verb in verbs]
            id_group = obj_relation.set_relation('synonym', None, *words)
            fasif['verbs'][language] = id_group

    return fasif


def process_word_combination(fasif, obj_relation, settings, path_import):
    not_to_db = ['nombr', 'cifer']

    get_condition = fasif['functions'].get('getCondition')
    get_condition_is_required = None
    if get_condition:
        get_condition['function'] = os.path.join(path_import, get_condition['function'])
        function = importer.import_action(get_condition['function'])
        get_condition_is_required = get_is_required(function)

    change_condition = fasif['functions'].get('changeCondition')
    change_condition_is_required = None
    if change_condition:
        change_condition['function'] = os.path.join(path_import, change_condition['function'])
        function = importer.import_action(change_condition['function'])
        change_condition_is_required = get_is_required(function)

    if None not in (get_condition_is_required, change_condition_is_required):
        if get_condition_is_required != change_condition_is_required:
            raise Exception('arguments for `get_condition` and `change_condition` must be equals')

    is_required = get_condition_is_required or change_condition_is_required

    fasif['argdescr'] = {}
    for language in settings.languages:
        message = Message(settings, fasif['wcomb'][language])
        wcomb = nature2internal(message, analyzers=analyzers)(0)

        for arg_name, args in fasif['args'].items():
            argwords = args['argwords'][language]
            argwords['name'] = get_dword(argwords['name'], settings)
            wcomb.chmanyByValues(
                {'argname': arg_name},
                setstring='subiv:noignore',
                base=argwords['name'].get('base'),
                case=argwords['name'].get('case')
            )
            argword = list(wcomb.getByValues(setstring='subiv:noignore', argname=arg_name))[0]
            bases = [argword[1] if argword[1] else argword[2][0]]
            argtables = args['argtable'].setdefault(language, {})
            for arg_word, argtable in argtables.copy().items():
                del argtables[arg_word]
                arg_word = get_dword(arg_word, settings)
                bases.append(arg_word)
                argtables[arg_word['base']] = argtable

            for index_hyperonym, hyperonym in enumerate(argwords['hyperonyms']):
                word_hyperonym = get_dword(hyperonym, settings)
                argwords['hyperonyms'][index_hyperonym] = word_hyperonym.getUnit('dict')
                if word_hyperonym['base'] not in not_to_db:
                    obj_relation.set_relation('hyperonym', word_hyperonym, *bases)

        for destination, value in fasif['functions'].items():
            verbs = value['verbs'].setdefault(language, {})
            for index, word_verb in enumerate(verbs):
                verbs[index] = obj_relation.set_relation('synonym', None, get_dword(word_verb, settings))

        fasif['argdescr'][language] = {}
        for argname, data in fasif['args'].items():
            fasif['argdescr'][language][argname] = {
                'isreq': is_required[argname],
                'argtable': data['argtable'][language],
                'hyperonyms': data['argwords'][language]['hyperonyms']
            }

        del fasif['args']
        fasif['wcomb'][language] = wcomb.getUnit('dict')

    return fasif


def fasif_parser(path_import, settings):
    obj_relation = Relation(settings)  # TODO: вместо этого получать отношения, вызывая методы слова
    for fasif_file_name in os.listdir(path_import):
        if fasif_file_name.endswith('.json'):
            with open(os.path.join(path_import, fasif_file_name), encoding='utf-8') as fasif_file:
                fasifs = json.load(fasif_file)
                for fasif in fasifs:
                    fasif_processor = 'process_{}'.format(fasif["type"])
                    fasif_processor = globals()[fasif_processor]
                    fasif = fasif_processor(fasif, obj_relation, settings, path_import)
                    if fasif:
                        settings.database.save_fasif(fasif["type"], fasif)
