import inspect

import yaml

from manspy.storage.relation import Relation
from manspy.utils import importer
from manspy.utils.constants import CASE
from manspy.runners.only_lingvo import runner


def get_is_required(func):
    if not func.__code__.co_argcount:
        raise Exception(f'The function "{func.__name__}" must have 1 or more arguments')

    first_arg_name = func.__code__.co_varnames[0]
    signature = inspect.signature(func)
    is_required = {}
    for arg_name, arg in signature.parameters.items():
        if arg_name == first_arg_name:
            continue

        is_required[arg_name] = arg.default is inspect.Parameter.empty

    return is_required


def get_dword(str_word, settings):
    text = runner(str_word, settings, pipeline=':postmorph')
    return text.first_child.first_child


def process_verb(fasif, obj_relation, settings):
    for language in settings.supported_languages:
        verbs = fasif['verbs'].get(language)
        if verbs:
            verbs = (get_dword(str_verb, settings) for str_verb in verbs)
            id_group = obj_relation.set_relation('synonym', None, *verbs)
            fasif['verbs'][language] = id_group

    return fasif


def process_word_combination(fasif, obj_relation, settings):
    not_to_db = ['nombr', 'cifer']

    fasif['argdescr'] = {}
    for language in settings.supported_languages:
        str_wcomb = fasif['wcomb'][language]
        if not str_wcomb:
            continue

        wcomb = runner(str_wcomb, settings, pipeline=':synt').first_child

        for arg_name, args in fasif['args'].items():
            argwords = args['argwords'][language]
            argwords['name'] = get_dword(argwords['name'], settings)
            wcomb.chmany_by_values(
                new_properties={'argname': arg_name},
                properties={'base': argwords['name']['base'], CASE: argwords['name'][CASE]},
                setstring='subiv:noignore',
            )
            argword = list(wcomb.get_by_values(properties={'argname': arg_name}, setstring='subiv:noignore'))[0]
            bases = [argword[1] if argword[1] else argword[2][0]]
            argtables = args['argtable'].setdefault(language, {})
            for arg_word, argtable in argtables.copy().items():
                del argtables[arg_word]
                arg_word = get_dword(arg_word, settings)
                bases.append(arg_word)
                argtables[arg_word['base']] = argtable

            for index_hyperonym, hyperonym in enumerate(argwords['hyperonyms']):
                word_hyperonym = get_dword(hyperonym, settings)
                argwords['hyperonyms'][index_hyperonym] = word_hyperonym.export_unit()
                if word_hyperonym['base'] not in not_to_db:
                    obj_relation.set_relation('hyperonym', word_hyperonym, *bases)

        is_required = None
        for value in fasif['functions'].values():
            str_verbs = value['verbs'].setdefault(language, [])
            for index, word_verb in enumerate(str_verbs):
                str_verbs[index] = obj_relation.set_relation('synonym', None, get_dword(word_verb, settings))

            function = importer.import_action(value['function'])
            current_is_required = get_is_required(function)
            if is_required is None:
                is_required = current_is_required
            elif is_required != current_is_required:
                raise Exception(
                    'Count and requirement of arguments for `get_condition` and `change_condition` must be equals',
                )

        fasif['argdescr'][language] = {}
        for argname, data in fasif['args'].items():
            fasif['argdescr'][language][argname] = {
                'isreq': is_required[argname],
                'argtable': data['argtable'][language],
                'hyperonyms': data['argwords'][language]['hyperonyms']
            }

        del fasif['args']
        fasif['wcomb'][language] = wcomb.export_unit()

    return fasif


def parse(fasif_path, settings):
    obj_relation = Relation(settings)  # TODO: вместо этого получать отношения, вызывая методы слова
    with open(fasif_path, encoding='utf-8') as fasif_file:
        for fasif in yaml.safe_load(fasif_file):
            fasif_processor = 'process_{}'.format(fasif["type"])
            fasif_processor = globals()[fasif_processor]
            fasif = fasif_processor(fasif, obj_relation, settings)
            if fasif:
                settings.database.save_fasif(fasif["type"], fasif)
