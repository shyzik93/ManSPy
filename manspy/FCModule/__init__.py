""" Модуль-обёртка для интеллекта
Все функции должны возвращать ответ: строка или список строк
"""


def run_wcomb_function(internal_sentence, arg0, function_name, prefix=''):
    """
    Выполняем функции словосочетаний:
    - получения состояния - для глаголов 1-го типа
    - изменения состояния - для глаголов 2-го типа
    :param internal_sentence:
    :param arg0:
    :param function_name:
    :param prefix:
    :return: генератор с ответами
    """
    for word_combination in internal_sentence['{}word_combinations'.format(prefix)]:
        for argument in word_combination['arguments']:
            for r_text in word_combination[function_name](arg0, **argument):
                yield r_text


def execute_internal_sentence(internal_sentence):
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

        if internal_sentence['verb']['func_common']:  # для глагола 1-го типа
            gen_r_texts = run_wcomb_function(internal_sentence, arg0, 'func_get_value')
            gen_r_texts = internal_sentence['verb']['func_common'](arg0, gen_r_texts)
        else:
            gen_r_texts = run_wcomb_function(internal_sentence, arg0, 'func_set_value')

        return gen_r_texts

    elif internal_sentence['type_sentence'] == 'fact':

        arg0 = {
            'antonym': internal_sentence['verb']['used_antonym'],
            # только для функции изменения состояния и ф-ции глагола
            'answer_type': internal_sentence['verb']['answer_type']
        }

        gen_r_texts = run_wcomb_function(internal_sentence, arg0, 'func_get_value', 'subjects_')

        return gen_r_texts

    elif internal_sentence['type_sentence'] == 'construction-condition':

        arg0 = {
            'antonym': internal_sentence['verb']['used_antonym'],
            # только для функции изменения состояния и ф-ции глагола
            'answer_type': internal_sentence['verb']['answer_type']
        }

        gen_r_texts = run_wcomb_function(internal_sentence, arg0)  # пока поддерживается лишь одно словосочетание
        for r_text in gen_r_texts:
            break


def execute_internal_sentences(ils, send_to_out):
    """
    Выполняет внутренние предложения в тексте поочерёдно, если есть условия и наречия - обусловленно.
    :param ils:
    :param send_to_out:
    :return:
    """
    for index_sentence, internal_sentence in ils.items():
        gen_r_texts = execute_internal_sentence(internal_sentence)
        for r_text in gen_r_texts:
            send_to_out(r_text)
