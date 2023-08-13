# -*- coding: utf-8 -*-
''' Модуль выполняет синтаксический анализ предложения.

  Определяются члены предложения, и устанавливаются связи слов.
'''

from manspy.utils.constants import (
    ADJECTIVE, ADVERB, ACCUSATIVE,
    CASE, CARDINAL, CATEGORY, CIRCUMSTANCE, CLASS, CONJUNCTION,
    DEFINITION, DIRECT_SUPPLEMENT,
    MOSENTENCE,
    NOMINATIVE, NOUN, NUMERAL,
    PERSONAL, POSPEECH, POSSESSIVE, PREDICATE, PRONOUN,
    SUBJECT, SUPPLEMENT,
    VERB,
)


def forPronounAndNoun(word):
    ''' Определяет член предложения для имени существительного
        и притяжательного местоимепния по падежу '''
    if word[CASE] == ACCUSATIVE:
        return DIRECT_SUPPLEMENT
    elif word[CASE] == NOMINATIVE:
        return SUBJECT
    return SUPPLEMENT


def setMOS_ToSign(feature_words):
    """ Определение члена предложения у признаков:
        прилагательного, наречия, """
    for feature in feature_words:
        if feature[POSPEECH] == ADJECTIVE or (feature[POSPEECH] == PRONOUN and feature[CATEGORY] == POSSESSIVE) or feature[POSPEECH] == NUMERAL:
            feature[MOSENTENCE] = DEFINITION
        elif feature[POSPEECH] == ADVERB:
            feature[MOSENTENCE] = CIRCUMSTANCE

        if feature.features:
            setMOS_ToSign(feature.features)

def setMOSentence(word):
    if word[POSPEECH] == VERB:
        word[MOSENTENCE] = PREDICATE
        if word.features:
            setMOS_ToSign(word.features)

    #ATTENTION обстоятельства, выраженные существительным, определяются в модуле
    # промежуточного анализа как наречие.
    elif word[POSPEECH] == NOUN or (word[POSPEECH] == NUMERAL and word[CLASS] == CARDINAL):
        word[MOSENTENCE] = forPronounAndNoun(word)
        if word.features:
            setMOS_ToSign(word.features)

    elif word[POSPEECH] == PRONOUN:
        if word[CATEGORY] == POSSESSIVE:
            word[MOSENTENCE] = DEFINITION  # ? Появилось определение
        elif word[CATEGORY] == PERSONAL:
            word[MOSENTENCE] = forPronounAndNoun(word)
        else:
            word[MOSENTENCE] = ''  # не притяжательное и не личное местоимение

    # прилагательное без существительного
    elif 'praPOSpeech' in word and word['praMOSentence'] == 'freemember':
        word[MOSENTENCE] = SUPPLEMENT
    #elif word[POSPEECH] == ADJECTIVE: word[MOSENTENCE] = DEFINITION
    else:
        word[MOSENTENCE] = ''


def setLinks(word, sentence):
    ''' Устанавливает связи членов предложения. Обстоятельства и определения
        спрятаны в тех, к кому они относятся. Работаем лишь со сказуемым,
        подлежащим и дополнением. '''
    if word[MOSENTENCE] == PREDICATE:
        # линкуем сказуемое и прямое дополнение
        old_position = sentence.position
        for word2 in sentence.iterFromByStep(1):
            if word2[MOSENTENCE] == DIRECT_SUPPLEMENT:
                sentence.addLink(word, word2)
            elif word2[MOSENTENCE] == PREDICATE:
                break

        sentence.position = old_position

    #  TODO: если у прямого дополнения нескеолько дополнений, то они проигнорируются
    elif word[MOSENTENCE] in [DIRECT_SUPPLEMENT, SUPPLEMENT, SUBJECT]:
        # линкуем прямое дополнение и следующее после него косвенное дополнение
        old_position = sentence.position
        case = None
        for word2 in sentence.iterFromByStep(1):
            if word2[MOSENTENCE] == SUPPLEMENT:# and word2[CASE] != "":
                """# остальные падежи, вероятно, будут означать, что косв. дополнение -
                # это обстоятельство, то есть относится к сказуемому.
                #if sentence(index2, CASE) in [GENETIVE]: sentence.addLink(index, index2)#word.links.append(index2)"""
                if not case:
                    case = word[CASE]
                sentence.addLink(word, word2)
            elif word2[MOSENTENCE] in [DIRECT_SUPPLEMENT, SUBJECT]:
                break  # это другой актант уже пойдёт.

        sentence.position = old_position


def go_throw_links(word, words=None):
    if words is None:
        words = []

    if word not in words:
        words.append(word)
    
        for link_word in word.links:
            go_throw_links(link_word, words)

        for homogeneous_link in word.homogeneous_links:
            go_throw_links(homogeneous_link, words)

    return words


# TODO: функция недописана
def split_sentence(sentence):

    # manspy2 exec --synt "se dolara kurzo de laboro estas kvaron"
    # manspy2 exec --synt "se dolara kurzo de laboro estas kvaro"
    # manspy2 exec --synt "se dolara kurzo de laboro estas 4"

    first_words = sentence.get_indexes_of_first_words()

    conjunctions = []
    subjects = []
    predicates = []

    _sentences = []

    for first_word in first_words:
        if first_word[POSPEECH] == CONJUNCTION:
            conjunctions.append(first_word) # сочинённых союзов между однородными членами должны исчезнуть в предыдущих шагах.
        if first_word[MOSENTENCE] == SUBJECT:
            subjects.append(first_word)
        if first_word[MOSENTENCE] == PREDICATE:
            predicates.append(first_word)

    for subject in subjects:
        _sentences.append(go_throw_links(subject))

    # определяем, в каком 
    for conjunction in conjunctions:
        sentence.jumpByIndex(conjunction.index)
        left, right = sentence.getNeighbours()

    #for index, word in sentence:
    #    left, right = sentence.getNeighbours()


def analyze(message):
    for sentence in message.text:
        # определяет члены предложения
        for word in sentence:
            setMOSentence(word)
        # устанавливает связи членов предложения
        for word in sentence:
            setLinks(word, sentence)

        # разделяем сложноподчинённые и сложносочинённые предложения
        split_sentence(sentence)

    return message.text
