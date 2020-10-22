""" Модуль-обёртка для интеллекта
Все функции должны возвращать ответ: строка или список строк
"""


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

        gen_r_texts = run_wcomb_function(internal_sentence, arg0)
        if internal_sentence['verb']['func_common']:  # для глагола 1-го типа
            gen_r_texts = internal_sentence['verb']['func_common'](arg0, gen_r_texts)
        return gen_r_texts

    elif internal_sentence['type_sentence'] == 'fact':
        pass
    elif internal_sentence['type_sentence'] == 'construction':
        pass


def execute_internal_sentences(ils, to_IF):
    """
    Выполняет поочерёдно внутренние предложения в тексте, если есть условия и наречия - обусловленно.
    :param ils:
    :param to_IF:
    :return:
    """
    for index_sentence, internal_sentence in ils.items():   # TODO: msg.ils должен содержать только внутренние предложения, не списки с предложениями
        gen_r_texts = execute_internal_sentence(internal_sentence)
        for r_text in gen_r_texts:
            to_IF(r_text)
    return []
