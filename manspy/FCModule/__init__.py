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
        return action['common_verb_function'](arg0, *[i for i in r_texts])


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


def execIL(ils, to_IF):
    for index_sentence, ILs in ils.items():   # TODO: msg.ils должен содержать только внутренние предложения, не списки с предложениями
        if ILs:
            LogicKernel(ILs, to_IF)
    return []
