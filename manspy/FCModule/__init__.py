""" Модуль-обёртка для интеллекта
Все функции должны возвращать ответ: строка или список строк
"""

from itertools import chain


def run_assoc_func(arg0, subject, action, arguments):
    """ Вызывает функцию, согласно обстоятелствам вызова """

    if action['wcomb_verb_function'] is not None:
        assoc_type = 'wcomb_verb_function'  # меняем состояние словосочетания
    else:
        assoc_type = 'wcomb_function'  # получаем состояние словосочетания

    if action['args_as_list'] == 'l':
        return action[assoc_type](arg0, *arguments)
    else:
        for argument in arguments:
            for r_text in action[assoc_type](arg0, **argument):
                yield r_text


def run_common_func(arg0, subject, action, arguments, r_texts):
    if action['wcomb_verb_function'] is not None:
        # ответ от функции, ассоциированной со словосочетанием и глаголом (измнили состояние словосочетания)
        return r_texts
    else:
        # ответ от функции, ассоциированной с глаголом
        return action['common_verb_function'](arg0, r_texts)


def LogicKernel(ILs, to_IF):
    """Главная функция. Работает только с ВЯ"""

    r_texts = []

    for IL in ILs:
        if IL['error_convert']['argument']:
            continue
        if not IL:
            continue

        action = IL['action']
        subject = IL['subject']
        arguments = IL['argument']
        arg0 = IL['arg0']

        if action['mood'] == 'imperative':
            # здесь можно проверить, кто дал приказ
            r_texts.append(run_assoc_func(arg0, subject, action, arguments))
        elif action['mood'] == 'indicative':
            # яв-предложение должно подаваться в функцию обработки фактов. А эта строчка - временная.
            r_texts.append(run_assoc_func(arg0, subject, action, arguments))

    for r_text in run_common_func(arg0, subject, action, arguments, chain(*r_texts)):
        to_IF(r_text)


def run_wcomb_function(internal_sentence, arg0):
    """
    Выполняем функции словосочетаний:
    - получения состояния - для глаголов 1-го типа
    - изменения состояния - для глаголов 2-го типа
    :param internal_sentence:
    :return: генератор с ответами
    """

    function_name = 'func_get_value' if internal_sentence['verb']['func_common'] else 'func_set_value'

    for word_combination in internal_sentence['word_combinations']:
        if word_combination['how_put_args'] == 'l':  # однородные передаются разом как позиционные аргументы
            yield word_combination[function_name](arg0, *word_combination['arguments'])
        else:  # однородные передаются по очереди как именованные
            for argument in word_combination['arguments']:
                for r_text in word_combination[function_name](arg0, **argument):
                    yield r_text


def exec_internal_sentence(internal_sentence):
    """
    Выполняет внутренние предложения.

    Для типа 'run':
    1. функции получения (для глагола 1-го типа) или изменения (для глагола 2-го типа) словосочетания
    2. функцию глагола - только для глагола 1-го типа
    :param internal_sentence:
    :return: генератор с ответами
    """
    if internal_sentence['type_sentence'] == 'run':

        arg0 = {
            'antonym': internal_sentence['verb']['used_antonym'],
            # только для функции изменения состояния и ф-ции глагола
            'answer_type': internal_sentence['verb']['answer_type']
        }

        gen_r_texts = run_wcomb_function(internal_sentence, arg0)
        if internal_sentence['verb']['func_common']:  # для глагола 1-го типа
            gen_r_texts = internal_sentence['verb']['func_common'](arg0, gen_r_texts)
        return gen_r_texts

    elif internal_sentence['type_sentence'] == 'fact':
        pass
    elif internal_sentence['type_sentence'] == 'construction':
        pass


def execIL(ils, to_IF):
    """
    Выполняет поочерёдно внутренние предложения в тексте, если есть условия и наречия - обусловленно.
    :param ils:
    :param to_IF:
    :return:
    """
    for index_sentence, ILs in ils.items():   # TODO: msg.ils должен содержать только внутренние предложения, не списки с предложениями
        ILs, internal_sentence = ILs
        # if ILs:
        #     LogicKernel(ILs, to_IF)
        gen_r_texts = exec_internal_sentence(internal_sentence)
        for r_text in gen_r_texts:
            to_IF(r_text)
    return []
