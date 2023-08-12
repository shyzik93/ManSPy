# -*- coding: utf-8 -*-
''' Модуль выполняет синтаксический анализ предложения.

  Определяются члены предложения, и устанавливаются связи слов.
'''

from manspy.utils.constants import (
    ADJECTIVE, ADVERB,
    CASE, CIRCUMSTANCE, CONJUNCTION,
    DEFINITION, DIRECT_SUPPLEMENT,
    MOSENTENCE,
    NOMINATIVE, NOUN, NUMERAL,
    POSPEECH, PREDICATE, PRONOUN,
    SUBJECT, SUPPLEMENT,
    VERB,
)


def forPronounAndNoun(word):
    ''' Определяет член предложения для имени существительного
        и притяжательного местоимепния по падежу '''
    if word[CASE] == 'accusative':
        return DIRECT_SUPPLEMENT
    elif word[CASE] == NOMINATIVE:
        return SUBJECT
    return SUPPLEMENT


def setMOS_ToSign(features):
    """ Определение члена предложения у признаков:
        прилагательного, наречия, """
    for feature in features:
        if feature[POSPEECH] == ADJECTIVE or (feature[POSPEECH] == PRONOUN and feature['category'] == 'possessive') or feature[POSPEECH] == NUMERAL:
            feature[MOSENTENCE] = DEFINITION
        elif feature[POSPEECH] == ADVERB:
            feature[MOSENTENCE] = CIRCUMSTANCE
        if feature['feature']:
            setMOS_ToSign(feature['feature'])


def setMOSentence(word):
    if word[POSPEECH] == VERB:
        word[MOSENTENCE] = PREDICATE
        if word['feature']:
            setMOS_ToSign(word['feature'])

    #ATTENTION обстоятельства, выраженные существительным, определяются в модуле
    # промежуточного анализа как наречие.
    elif word[POSPEECH] == NOUN or (word[POSPEECH] == NUMERAL and word['class'] == 'cardinal'):
        word[MOSENTENCE] = forPronounAndNoun(word)
        if word['feature']:
            setMOS_ToSign(word['feature'])

    elif word[POSPEECH] == PRONOUN:
        if word['category'] == 'possessive':
            word[MOSENTENCE] = DEFINITION  # ? Появилось определение
        elif word['category'] == 'personal':
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
                #if sentence(index2, CASE) in [GENETIVE]: sentence.addLink(index, index2)#word['link'].append(index2)"""
                if not case:
                    case = word[CASE]
                sentence.addLink(word, word2)
            elif word2[MOSENTENCE] in [DIRECT_SUPPLEMENT, SUBJECT]:
                break  # это другой актант уже пойдёт.

        sentence.position = old_position


def goThrowLinks(index, sentence, indexes=None):

    if indexes is None:
        indexes = []

    if index not in indexes:
        indexes.append(index)
    
        for index_link in sentence[index]['link']:
            goThrowLinks(index_link, sentence, indexes)
        for index_link in sentence[index]['homogeneous_link']:
            goThrowLinks(index_link, sentence, indexes)    

    return indexes


# TODO: функция недописана
def split_sentence(sentence):

    # manspy2 exec --synt "se dolara kurzo de laboro estas kvaron"
    # manspy2 exec --synt "se dolara kurzo de laboro estas kvaro"
    # manspy2 exec --synt "se dolara kurzo de laboro estas 4"

    first_indexes = sentence.getIndexesOfFirstWords()
    #first_words = [sentence(i, 'word') for i in first_indexes]
    #print('        Root words of the sentence:', [sentence(i, 'word') for i in first_indexes])

    conjunctions = []
    subjects = []
    predicates = []

    _sentences = []

    for first_index in first_indexes:
        if sentence[first_index][POSPEECH] == CONJUNCTION:
            conjunctions.append(first_index) # сочинённых союзов между однородными членами должны исчезнуть в предыдущих шагах.
        if sentence[first_index]['POSentence'] == SUBJECT:
            subjects.append(first_index)
        if sentence[first_index]['POSentence'] == PREDICATE:
            predicates.append(first_index)    

    for subject in subjects:
        _sentences.append(goThrowLinks(subject, sentence))

    # определяем, в каком 
    for conjunction_index in conjunctions:
        sentence.jumpByIndex(conjunction_index)
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
