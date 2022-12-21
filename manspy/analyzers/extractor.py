def collect_by_link(sentence, word):
    """
    Вынимает все слова по ссылкам
    :param sentence: предложение, из которого происходит вынимание
    :param word: первоначальное слово в цепочке
    :return:
    """
    subsentence = {}
    while word['link']:
        subsentence[word['index']] = word
        word = sentence[word['link'][0]]

    subsentence[word['index']] = word
    return subsentence


def separate_argument(sentence, word, arguments, argument_indexes_for_delete):
    if word['MOSentence'] == 'direct supplement':
        argument = collect_by_link(sentence, word)
        arguments.append(argument)
        argument_indexes_for_delete.extend(list(argument.keys()))
    elif word['MOSentence'] == 'supplement':
        argument = collect_by_link(sentence, word)
        arguments.append(argument)
        argument_indexes_for_delete.extend(list(argument.keys()))
    else:
        pass  # print(word)


def _extract(sentence):
    """ Разбивает предложение на предикат и его актанты.
        Именга переменных здесь и далее в программе:
          argument - это актант, перевод на английский
          arg - это аргумент функции, имеет такойже первод на английский, как и актант"""
    arguments_by_predicate = []  # словосочетания (актанты)
    predicates = []
    predicate_indexes_for_delete = []
    argument_indexes_for_delete = []
    subjects_by_predicate = []
    subject_indexes_for_delete = []

    current_predicate_index = None
    arguments = None
    subjects = None
    orphan_words = []
    for index, word in sentence.itemsUnit():
        if word['MOSentence'] == 'subject':
            subjects = []
            subjects_by_predicate.append(subjects)
            subject = collect_by_link(sentence, word)
            subjects.append(subject)
            subject_indexes_for_delete.extend(list(subject.keys()))
        elif word['MOSentence'] == 'predicate':
            current_predicate_index = index
            arguments = []
            arguments_by_predicate.append(arguments)
            predicate_indexes_for_delete.append(current_predicate_index)
            predicates.append(word)

            if len(predicates) != len(subjects_by_predicate):
                subjects_by_predicate.append([])

            for orphan_word in orphan_words:
                separate_argument(sentence, orphan_word, arguments_by_predicate[-1], argument_indexes_for_delete)
                orphan_words.clear()

        if index in argument_indexes_for_delete or index in predicate_indexes_for_delete or index in subject_indexes_for_delete:
            continue

        if current_predicate_index is None:
            orphan_words.append(word)
            continue

        separate_argument(sentence, word, arguments, argument_indexes_for_delete)

    sentence.delByIndex(*subject_indexes_for_delete)  # TODO переделать в `del sentence[*subject_indexes_for_delete]`, а delByIndex - удалить
    sentence.delByIndex(*predicate_indexes_for_delete)
    sentence.delByIndex(*argument_indexes_for_delete)

    if sentence.getUnit("dict"):
        print("       Необработанные остатки 3 ФАСИФ \n", sentence.getUnit("dict"))
        print("-"*10)

    return subjects_by_predicate, predicates, arguments_by_predicate


def analyze(message):
    extracts = []
    for sentence in message.text:
        extracts.append(_extract(sentence))

    return extracts
