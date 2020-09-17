# -*- coding: utf-8 -*-

import sys, copy
from . import to_formule, NLModules, lingvo_math, Action
from manspy.utils import importer

"""
"""

not_to_db = ['nombr', 'cifer']

def is_in_hyperonym(hyperonyms, argvalue, R):
    for hyperonym in hyperonyms:
        if (hyperonym in not_to_db and isinstance(argvalue, (int, float, complex))) or \
            R.isRelBetween('hyperonym', hyperonym, argvalue): return True
    return False

def convert_by_argtable(fasif, argname, argvalue):
    if argvalue not in fasif['argdescr'][argname]['argtable']: return argvalue
    return fasif['argdescr'][argname]['argtable'][argvalue]

def check_args(finded_args, fasif, R):
    # Проверка на наличие в абстрактной группе
    hyperonyms = {}
    for argname, data in fasif['argdescr'].items():
        # пока только основные гиперонимы вытягиваем
        hyperonyms[argname] = [word['base'] for word in data['hyperonyms']]
    for finded_arg in finded_args:
        for argname, argvalue in list(finded_arg.items()):
            if not is_in_hyperonym(hyperonyms[argname], argvalue, R): del finded_arg[argname]

    # Проверка на отсутствие обязательных аргументных слов
    checked_args = []
    for finded_arg in finded_args:
        isright = True
        for argname, argdescr in fasif['argdescr'].items():
            if argname not in finded_arg and argdescr['isreq']: # если отсутствует обязательный аргумент
                isright = False
                break
        if isright: checked_args.append(finded_arg)

    # Конвертирование аргументных слов по таблице из фасифа
    for checked_arg in checked_args:
        for argname, argvalue in checked_arg.items():
            checked_arg[argname] = convert_by_argtable(fasif, argname, argvalue)
    return checked_args

def if_verb_in_fasif(fasif, id_group): # в фасифе можно сохранять список всех глаголов для всех назначений для уменьшения кол-ва вычислений
    for destination, data in fasif['functions'].items():
        if id_group in data['verbs']: return data['function']

def get_fasif_wcomb(fdb, argument, R, verb):
    compared_fasifs = fdb.getFASIF('WordCombination', argument)
    if not compared_fasifs: return
    else: id_fasif, data = list(compared_fasifs.items())[0] # если фасифов несколько, то необходимо отсеть лишние в этом месте (отдельной функцией)
    finded_args, fasif = data

    # Вынимаем функцию, ассоциированную с "глагол + словосочетание"
    id_group = R.R.get_groups_by_word('synonym', 0, verb['base'], 'verb')[0]

    isantonym = verb['antonym']
    function = if_verb_in_fasif(fasif, id_group)
    if function == None: # если глагол не найден, то пробуем антоним
        verb_synonym_group_id = R.R.get_words_from_samegroup('antonym', 'verb', 'synonym', id_group)
        id_antonym = id_group#func(verb_synonym_group_id) # дописать
        function = if_verb_in_fasif(fasif, id_antonym)
        if function != None: isantonym = not isantonym

    fasif['id'] = id_fasif
    return finded_args, fasif, function, isantonym

def Extraction2IL(R, settings, predicates, arguments):
    fdb = to_formule.FasifDB(settings.language)
    pattern_IL = {
        'arg0': {  # передаётся первым аргументом в каждую функцию
            'antonym': False,
            'answer_type': None,
        },
        'action': {
          'wcomb_function': None,      # функция, ассоциированная со словосочетанием. Ей передаются аргументные слова
          'common_verb_function': None,# функция, ассоциированная с глаголом. Её аргументы - возвращаемые значения предыдущей функции.
          'wcomb_verb_function': None, # функция, ассоциированная со связкой "словосочетание + глагол". Она принимает аргументные слова.
          'mood': '',
          'circumstance': '',
          'type circumstance': ''
          },
        'argument': [],
        'subject': None,
        'error_convert': {'function':[], 'argument':[]}
    }
    ILs = []
    predicate = list(predicates.values())[0]
    fasif_IL = {}

    # Вынимаем Фасиф
    for _argument in arguments:
        argument = NLModules.ObjUnit.Sentence(_argument)
        IL = copy.deepcopy(pattern_IL)
        res = get_fasif_wcomb(fdb, argument, R, predicate)
        if res is None:
            continue
        finded_args, fasif, function, isantonym = res
        #if 'antonym' in predicate and predicate['antonym'] != isantonym: IL['arg0']['antonym'] = True
        IL['arg0']['antonym'] = isantonym
        IL['arg0']['answer_type'] = settings.answer_type

        # Вынимаем фасиф словосочетания  # здевсь же отсеиваем неподходящие фасифы (через continue)
        for argname, args in finded_args.items():
            finded_args[argname] = list(set(args)) # отсеиваем повторы
            #if fasif['argdescr'][argname]['args_as_list'] == 'l': finded_args[argname] = [finded_args[argname]]
        finded_args = lingvo_math.dproduct(finded_args)
        finded_args = check_args(finded_args, fasif, R)
        with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
            flog.write('\n%s\n%s\n' % (str(finded_args), str(fasif['functions'])))

        # добавляем аргументные слова в ВЯ
        if fasif['id'] not in fasif_IL: fasif_IL[fasif['id']] = len(ILs) 
        else: # добавляем к уже существующему ВЯ для данного ФАСИФа
            ILs[fasif_IL[fasif['id']]]['argument'].extend(finded_args)
            continue
        IL['argument'] = finded_args
        IL['action']['args_as_list'] = fasif['argdescr'][argname]['args_as_list']

        if function: # если найдена функция, ассоциированная "глагол + словосочетание"
            IL['action']['wcomb_verb_function'] = importer.action(function)
        else: # иначе вынимаем функцию, ассоциированную с словосочетанием
            function = fasif['functions']['getCondition']['function']
            IL['action']['wcomb_function'] = importer.action(function)
            id_group = R.R.get_groups_by_word('synonym', 0, predicate['base'], 'verb')[0]
            compared_fasifs = fdb.getFASIF('Verb', id_group)
            if not compared_fasifs:
                sys.stderr.write('FASIF was not finded! Argument (word combination) is "'+str(argument)+'"')
                continue
            if not compared_fasifs: sys.stderr.write('Fasif for "%s" wasn\'t found!' % predicate['base'])
            # затем вынимаем общую функцию, ассоциированую с глаголом
            IL['action']['common_verb_function'] = importer.action(list(compared_fasifs.values())[0][0][0])

        with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
            flog.write('\npraIL: %s\n' % str(IL))

        IL['action']['mood'] = predicate['mood']
        ILs.append(IL)
        #fwcomb = to_formule.to_formule(argument, False)
        #print x, fdb.get_hashWComb(fwcomb)
    return ILs
