import sys
import copy
import itertools

from manspy.unit import Sentence
from manspy.fasif import finder
from manspy.utils import importer

not_to_db = ['nombr', 'cifer']


def dproduct(dparentl):
    """
    Выполняет декартово (прямое) произведение над словарями в списке dparent1
    В стандартной библиотеке Python я этой функции не нашёл.
    Функция необходима для аргументных слов.
    :param dparentl: {'a': [1,2], 'b': [5,6]}
    :return: [{'a': 1, 'b':5}, {'a': 1, 'b':6}, {'a': 2, 'b':5}, {'a': 2, 'b':6}]
    """
    def _dproduct(resl, values, key):
        """
        [
            (('a',1), ('b',5)),
            (('a',1), ('b',6)),
            (('a',2), ('b',5)),
            (('a',2), ('b',6))
        ]
        """
        n = len(values)
        _resl = list(resl)
        for i, el in enumerate(resl, 0):
            for j in range(n - 1):
                _resl.insert(i * n, dict(el))
            for j in range(n):
                _resl[j + n * i][key] = values[j]
        return _resl
    prevchildl = [{}]
    for key, values in dparentl.items():
        prevchildl = _dproduct(prevchildl, values, key)
    return prevchildl


def dproduct2(dparent1):
    """ Второй вариант функции. TODO: Необходимо обе протестировать на скорость """
    l = [([k], v) for k, v in dparent1.items()]
    l = [[i for i in itertools.product(*subl)] for subl in l]
    l = [i for i in itertools.product(*l)]
    l = [dict(i) for i in l]
    return l


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
            if argname not in finded_arg and argdescr['isreq']:  # если отсутствует обязательный аргумент
                isright = False
                break
        if isright: checked_args.append(finded_arg)

    # Конвертирование аргументных слов по таблице из фасифа
    for checked_arg in checked_args:
        for argname, argvalue in checked_arg.items():
            checked_arg[argname] = convert_by_argtable(fasif, argname, argvalue)
    return checked_args


def find_func_set_value(fasif, id_group): # в фасифе можно сохранять список всех глаголов для всех назначений для уменьшения кол-ва вычислений
    for destination, data in fasif['functions'].items():
        if id_group in data['verbs']:
            return data['function']


def Extraction2IL(R, settings, predicates, arguments):
    fdb = finder.FasifDB(settings.c, settings.cu)
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
    verb = {'func_common': None, 'used_antonym': False, 'answer_type': settings.answer_type}
    internal_sentence = {'type_sentence': 'fact', 'verb': verb, 'word_combinations': []}

    # определяем тип предложения

    if predicate['mood'] == 'imperative':
        internal_sentence['type_sentence'] = 'run'

    #  Выимаем ФАСИФ глагола

    id_group = R.R.get_groups_by_word('synonym', 0, predicate['base'], 'verb')[0]
    compared_fasifs = fdb.getFASIF('Verb', id_group)
    if compared_fasifs:
        verb['func_common'] = importer.action(list(compared_fasifs.values())[0][0][0])
    else:
        # TODO: проверить антоним (), как для функции изменения состояния
        pass

    # Вынимаем Фасиф
    for _argument in arguments:

        argument = Sentence(_argument)
        IL = copy.deepcopy(pattern_IL)  # excess

        # Вынимаем ФАСИФ словосочетания

        compared_fasifs = fdb.getFASIF('WordCombination', argument)
        if not compared_fasifs:
            continue
        id_fasif, data = list(compared_fasifs.items())[0]  # если фасифов несколько, то необходимо отсеть лишние в этом месте (отдельной функцией)
        finded_args, fasif = data

        # Вынимаем функцию получения/изменения состояния.

        id_group = R.R.get_groups_by_word('synonym', 0, predicate['base'], 'verb')[0]

        verb['used_antonym'] = predicate['antonym']
        func_get_value = fasif['functions']['getCondition']['function'] if 'getCondition' in fasif['functions'] else None
        func_set_value = find_func_set_value(fasif, id_group)
        if func_set_value is None:  # если глагол не найден, то пробуем антоним
            # TODO: добавить антонимы для примера через глагол-связку. Здесь затем искать по id группы антонимов
            verb_synonym_group_id = R.R.get_words_from_samegroup('antonym', 'verb', 'synonym', id_group)
            id_antonym = id_group
            func_set_value = find_func_set_value(fasif, id_antonym)
            if func_set_value:
                verb['used_antonym'] = not verb['used_antonym']
        word_combination = {
            'func_get_value': importer.action(func_get_value) if func_get_value else None,
            'func_set_value': importer.action(func_set_value) if func_set_value else None,
            'arguments': [],
        }

        #if 'antonym' in predicate and predicate['antonym'] != isantonym: IL['arg0']['antonym'] = True
        IL['arg0']['antonym'] = verb['used_antonym']   # excess
        IL['arg0']['answer_type'] = settings.answer_type  # excess

        # Вынимаем фасиф словосочетания  # здесь же отсеиваем неподходящие фасифы (через continue)
        for argname, args in finded_args.items():
            finded_args[argname] = list(args)  # TODO: #UNIQ_ARGS Нужны ли нам дубли аргументов?
            #if fasif['argdescr'][argname]['args_as_list'] == 'l': finded_args[argname] = [finded_args[argname]]
        finded_args = dproduct(finded_args)
        finded_args = check_args(finded_args, fasif, R)
        with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:  # excess
            flog.write('\n%s\n%s\n' % (str(finded_args), str(fasif['functions']))) # exxcess

        # добавляем аргументные слова в ВЯ
        if id_fasif not in fasif_IL:
            fasif_IL[id_fasif] = len(ILs)
        else:  # добавляем к уже существующему ВЯ для данного ФАСИФа
            ILs[fasif_IL[id_fasif]]['argument'].extend(finded_args)
            continue
        word_combination['arguments'] = finded_args
        word_combination['how_put_args'] = fasif['argdescr'][argname]['args_as_list']
        IL['argument'] = finded_args  # excess
        IL['action']['args_as_list'] = fasif['argdescr'][argname]['args_as_list']  # excess

        if func_set_value:  # если найдена функция, ассоциированная "глагол + словосочетание"
            IL['action']['wcomb_verb_function'] = importer.action(func_set_value)  # excess
        else:  # иначе вынимаем функцию, ассоциированную с словосочетанием
            func_set_value = fasif['functions']['getCondition']['function']  # excess
            IL['action']['wcomb_function'] = importer.action(func_set_value)  # excess
            id_group = R.R.get_groups_by_word('synonym', 0, predicate['base'], 'verb')[0]  # excess
            compared_fasifs = fdb.getFASIF('Verb', id_group)  # excess
            if not compared_fasifs:  # excess
                sys.stderr.write('FASIF was not finded! Argument (word combination) is "'+str(argument)+'"')  # excess
                continue  # excess
            if not compared_fasifs:  # excess
                sys.stderr.write('Fasif for "%s" wasn\'t found!' % predicate['base'])  # excess
            # затем вынимаем общую функцию, ассоциированую с глаголом  # excess
            IL['action']['common_verb_function'] = importer.action(list(compared_fasifs.values())[0][0][0])  # excess

        with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
            flog.write('\npraIL: %s\n' % str(IL))

        IL['action']['mood'] = predicate['mood']  # excess
        ILs.append(IL)  # excess
        #fwcomb = to_formule.to_formule(argument, False)
        #print x, fdb.get_hashWComb(fwcomb)
        internal_sentence['word_combinations'].append(word_combination)
    return ILs, internal_sentence  # excess


def convert(sentences, OR, settings):
    internal_sentences = {}
    for index, sentence in enumerate(sentences):
        predicates, arguments = sentence
        internal_sentences[index] = Extraction2IL(OR, settings, predicates, arguments)
    return internal_sentences
