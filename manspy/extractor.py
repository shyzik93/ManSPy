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
        word = sentence(word['link'][0])

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
    predicate_indexes = []
    argument_indexes_for_delete = []

    current_predicate_index = None
    arguments = None
    orphan_words = []
    for index, word in sentence.itemsUnit():
        if word['MOSentence'] == 'predicate':
            current_predicate_index = index
            arguments = []
            arguments_by_predicate.append(arguments)
            predicate_indexes.append(current_predicate_index)
            predicates.append(word)

            for orphan_word in orphan_words:
                separate_argument(sentence, orphan_word, arguments_by_predicate[-1], argument_indexes_for_delete)
                orphan_words.clear()

        if index in argument_indexes_for_delete or index in predicate_indexes:
            continue

        if current_predicate_index is None:
            orphan_words.append(word)
            continue

        separate_argument(sentence, word, arguments, argument_indexes_for_delete)

    sentence.delByIndex(*argument_indexes_for_delete)
    sentence.delByIndex(*predicate_indexes)

    if sentence.getUnit("dict"):
        print(u"       Необработанные остатки 3 ФАСИФ \n", sentence.getUnit("dict"))
        print("-"*10)

    return predicates, arguments_by_predicate


def extract(sentences):
    extracts = []
    for index, sentence in sentences:
        extracts.append(_extract(sentence))

    return extracts
