# -*- coding: utf-8 -*-
''' Модуль выполняет расширенный морфологический разбор слова,
    то есть на основе связей в предложении.
    По завершению удаляются все служебные части речи.
    Можно приступать к синтаксичекому анализу предложения.
    '''
from manspy.utils.constants import (
    ADJECTIVE, ADVERB, ARTICLE,
    CASE, CONJUNCTION, COORDINATING,
    NOUN, NUMERAL,
    POSPEECH, PREPOSITION, PRONOUN,
    VALUE, VERB,
)


def process_article(word, sentence):
    if word[POSPEECH] == ARTICLE:
        sentence.delByStep()  # пока только удаляем


def process_preposition(word, sentence):
    if word[POSPEECH] != PREPOSITION:
        return

    left, right = sentence.getNeighbours()
    if right is None:
        sentence.delByStep()

    elif right[POSPEECH] in [NOUN, PRONOUN, NUMERAL]:
        sentence.getByStep(1)[CASE] = word['give_case']
        sentence.delByStep()
    else:
        sentence.error.add("postmorph", 'After preposition "'+word['word']+'" must be a noun or a pronoun or a cardinal numeral! Found '+str(sentence.getByStep(1)), 0)


def process_conjunction(word, sentence):
    if word[POSPEECH] != CONJUNCTION or word[VALUE] != COORDINATING:
        return

    left, right = sentence.getNeighbours()
    if left is None or right is None:  # если союз первый или последний в предложении
        sentence.delByStep()

    # сочинительный союз
    #if word['word'] == 'kaj': # заменить логическими символами (kaj = &)
    #print word['base']
    if left[POSPEECH] == right[POSPEECH] or \
         (left[POSPEECH] == NOUN and right[POSPEECH] == PRONOUN and right['category'] != 'possessive') or (right[POSPEECH] == NOUN and left[POSPEECH] == PRONOUN and left['category'] != 'possessive') or \
         ((left[POSPEECH] == PRONOUN and left['category'] == 'possessive') and right[POSPEECH] == ADJECTIVE) or ((right[POSPEECH] == PRONOUN and right['category'] == 'possessive') and left[POSPEECH] == ADJECTIVE) or \
         (left[POSPEECH] == NOUN and 'praMOSentence' in right and right['praMOSentence'] == 'freemember' and right[POSPEECH] == NUMERAL):
         #((left[POSPEECH] in [PRONOUN, ADJECTIVE] and ('category' in left and left['category'] == 'possessive')) and right[POSPEECH] in [PRONOUN, ADJECTIVE]):
    #if (CASE in left and CASE in right) and left[CASE] == right[CASE]:
        if (CASE in right and right[CASE] == 'accusative') and (CASE in left and left[CASE] != 'accusative'):
            sentence.delByStep(jump_step=0)
            return

        # устанавливаем однородность
        sentence.addHomogeneous(-1, 1) # для дополнений
        sentence.delByStep() # удаляем союз
    #elif left[POSPEECH] == NOUN and right[POSPEECH] == PREPOSITION:
    # Однородности нужны лишь для дополнения связей. В коверторе должны фигурировать лишь связи, но не однородности!


def mark_freemembers(sentence, indexes):
    for index in indexes:
        sentence[index]['praMOSentence'] = 'freemember'
    #sentence.addHomogeneous(*indexes) # не совсем корректно
    #sentence.jumpByStep(-len(indexes))


def process_definition(word, sentence, indexes=None):
    if indexes is None:
        indexes = []

    if word[POSPEECH] == ADJECTIVE or (word[POSPEECH] == PRONOUN and word['category'] == 'possessive') or word[POSPEECH]==NUMERAL:
        indexes.append(sentence.getByStep().index)
        if sentence.isLast():
            mark_freemembers(sentence, indexes)
            return # завершаем цикл, ибо прилагательные без существительного. Их мы не удаляем, так как они могут следовать после глагола esti

        sentence.jumpByStep()
        process_definition(sentence.getByStep(), sentence, indexes)
    elif word[POSPEECH] in [NOUN] and indexes: # если перед существительным стояли прилагательные
        sentence.addFeature(sentence.getByStep().index, *indexes)
        sentence.jumpByStep(-len(indexes))
    else:
        mark_freemembers(sentence, indexes)


def checkAdverbBefore(sentence):
    if sentence.position + 1 >= len(sentence):
        return False  # т. е. является последним

    # if adverb['base'] == u'ankaŭ': # стоит перед словом, к которому относится
    return sentence.getByStep(1)[POSPEECH] in [VERB, ADJECTIVE, ADVERB]


def checkAdverbAfter(sentence):
    if sentence.isFirst():
        return False

    return sentence.getByStep(-1)[POSPEECH] in (VERB, ADJECTIVE, ADVERB)


def process_adverb(word, sentence):
    if sentence.getByStep()[POSPEECH] != ADVERB:
        return

    index = sentence.getByStep().index
    if checkAdverbBefore(sentence):  # порядок менять не рекомендуется: покажи ОЧЕНЬ СИНИЙ цвет.
        # ПОКАЖИ БЫСТРО синий цвет - а вот здесь необходимо расставлять приоритеты для прилагательных и глаголов.
        # БЫСТРО - относится только к глаголам,
        # ПОКАЖИ ОЧЕНЬ синий цвет - стоит перед словом, к которому относится (глагол, наречие, прил)
        # ХОЧУ ОЧЕНЬ СИЛЬНО ; ХОЧУ ОЧЕНЬ - одно и тоже, но в первом случае
        # ОЧЕНЬ относится к СИЛЬНО, а СИЛЬНО - к глаголу. В овтором случае - ОЧЕНЬ относится к глаголу.
        # то есть, одни наречия для прилагательных, другие - для глаголов.
        sentence.addFeature(index+1, index)
    elif checkAdverbAfter(sentence):
        sentence.addFeature(index-1, index)
        sentence.jumpByStep(-1)
    else:
        old_position = sentence.position
        for word in sentence:  # "свободноплавающее" нарчие. Добавим его к глаголу.
            if word[POSPEECH] == VERB:
                sentence.addFeature(word.index, index) #EX_ERROR если последний  index2, то возникает интересная рекурсивная ошибка.
                break

        sentence.position = old_position
        #Error print index бесконечный цикл, если в предложении одни только наречия. Решение - сделать добавление мнимых слов.


def exchangeDataBetweenHomo(sentence):
    done_indexes = []
    for word in sentence:
        if word.index in done_indexes:
            continue

        for index_homo in word['homogeneous_link']:
            if CASE in word:
                sentence[index_homo][CASE] = word[CASE]

            done_indexes.append(index_homo)


def numeral2number(sentence, indexes):
    """ Числительное в число """
    glued_numeral = ' '.join([sentence[index]['word'] for index in indexes])
    numeral_value = 0
    multiplier = 1
    temp_sum = 0
    indexes.reverse()
    first_iter = True
    for index in indexes:
        nv = sentence[index]['number_value']
        if nv > 999:
            if temp_sum == 0 and not first_iter:
                temp_sum = 1

            numeral_value += temp_sum * multiplier
            temp_sum = 0
            multiplier = nv
        else:
            temp_sum += nv

        first_iter = False

    if temp_sum == 0:
        temp_sum = 1

    numeral_value += temp_sum * multiplier
    indexes.reverse()
    return numeral_value, glued_numeral


def process_numeral(word, sentence, indexes=None):
    if indexes is None:
        indexes = []

    if word[POSPEECH] == NUMERAL or (word[POSPEECH] == NOUN and 'derivative' in word and word['derivative'] == NUMERAL):
        indexes.append(sentence.getByStep().index)
        if not sentence.isLast():
            sentence.jumpByStep()
            process_numeral(sentence.getByStep(), sentence, indexes)
            return

    if len(indexes) <= 1:
        return

    # "Склейка" числительных
    ########## необязательное TASK: индексы в списке заменить на слова! #################333

    #print indexes
    numeral_value, glued_numeral = numeral2number(sentence, indexes)
    #print numeral_value, glued_numeral,
    word_index = indexes[-1]
    sentence[word_index]['word'] = glued_numeral
    sentence[word_index]['number_value'] = numeral_value
    sentence[word_index]['base'] = ''
    sentence.delByIndex(*indexes[:-1])
    sentence.jumpByStep(-len(indexes))


def analyze(message):
    ''' Обёртка '''
    for sentence in message.text:
        #TASK обстоятельства, выраженные существительным, обозначить как наречие
        processors = [
            process_numeral,
            process_article,
            process_conjunction,
            process_adverb,
            process_conjunction,
            process_definition,
            process_conjunction,
            process_preposition,
            process_conjunction
        ]
        for processor in processors:
            for word in sentence:
                processor(word, sentence)
        exchangeDataBetweenHomo(sentence)  # копируем характеристики с первого однородного ко последующим ему однородным.

        # здесь нужно найти однородные косвенные дополнения, чтобы им установить однородность.
        # При синтаксическом анализе на них будет ссылаться их родитель.

    return message.text
