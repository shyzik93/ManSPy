from manspy.utils.constants import DIRECT_SUPPLEMENT, MOSENTENCE, PREDICATE, SUBJECT, SUPPLEMENT


def collect_by_link(word):
    """
    Вынимает все слова по ссылкам
    :param word: первоначальное слово в цепочке
    :return:
    """
    subsentence = {}
    word.remove(-1)
    while word.links:
        subsentence[word.index] = word
        word = word.links[0]
        word.remove()

    subsentence[word.index] = word
    return subsentence


def separate_argument(word, arguments, argument_indexes_for_delete):
    if word[MOSENTENCE] in (SUPPLEMENT, DIRECT_SUPPLEMENT):
        argument = collect_by_link(word)
        arguments.append(argument)
        argument_indexes_for_delete.extend(list(argument.keys()))


def _extract(sentence):
    """ Разбивает предложение на предикат и его актанты.
        Именга переменных здесь и далее в программе:
          argument - это актант, перевод на английский
          arg - это аргумент функции, имеет такойже первод на английский, как и актант"""
    arguments_by_predicate = []  # словосочетания (актанты)
    predicates = []
    argument_indexes_for_delete = []
    subjects_by_predicate = []

    current_predicate_index = None
    arguments = None
    subjects = None
    words_before_predicate = []
    for word in sentence:
        if word[MOSENTENCE] == SUBJECT:
            subjects = []
            subjects_by_predicate.append(subjects)
            subject = collect_by_link(word)
            subjects.append(subject)
        elif word[MOSENTENCE] == PREDICATE:
            arguments = []
            arguments_by_predicate.append(arguments)
            predicates.append(word)
            word.remove(-1)
            current_predicate_index = word.index

            if len(predicates) != len(subjects_by_predicate):
                subjects_by_predicate.append([])

            for orphan_word in words_before_predicate:
                separate_argument(orphan_word, arguments_by_predicate[-1], argument_indexes_for_delete)

            words_before_predicate.clear()
        else:
            if word.index in argument_indexes_for_delete:
                continue

            if current_predicate_index is None:
                words_before_predicate.append(word)
                continue

            separate_argument(word, arguments, argument_indexes_for_delete)

    if sentence:  # TODO: сделать массив в Message для добавления уведомлений
        print("       Необработанные остатки 3 ФАСИФ \n", sentence.export_unit())
        print("-"*10)

    return subjects_by_predicate, predicates, arguments_by_predicate


def analyze(message):
    extracts = []
    for sentence in message.text:
        extracts.append(_extract(sentence))

    return extracts
