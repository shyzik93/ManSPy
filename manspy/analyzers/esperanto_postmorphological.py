# -*- coding: utf-8 -*-
''' Модуль выполняет расширенный морфологический разбор слова,
    то есть на основе связей в предложении.
    По завершению удаляются все служебные части речи.
    Можно приступать к синтаксичекому анализу предложения.
    '''
from manspy.utils.constants import (
    ADJECTIVE, ADVERB, ARTICLE,
    CASE, CATEGORY, CONJUNCTION, COORDINATING,
    DERIVATIVE,
    NOUN, NUMERAL,
    POSPEECH, POSSESSIVE, PREPOSITION, PRONOUN,
    CONJUNCTION_VALUE, VERB,
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
    if word[POSPEECH] != CONJUNCTION or word[CONJUNCTION_VALUE] != COORDINATING:
        return

    left, right = sentence.getNeighbours()
    if left is None or right is None:  # если союз первый или последний в предложении
        sentence.delByStep()

    # сочинительный союз
    #if word['word'] == 'kaj': # заменить логическими символами (kaj = &)
    #print word['base']
    if left[POSPEECH] == right[POSPEECH] or \
         (left[POSPEECH] == NOUN and right[POSPEECH] == PRONOUN and right[CATEGORY] != POSSESSIVE) or (right[POSPEECH] == NOUN and left[POSPEECH] == PRONOUN and left[CATEGORY] != POSSESSIVE) or \
         ((left[POSPEECH] == PRONOUN and left[CATEGORY] == POSSESSIVE) and right[POSPEECH] == ADJECTIVE) or ((right[POSPEECH] == PRONOUN and right[CATEGORY] == POSSESSIVE) and left[POSPEECH] == ADJECTIVE) or \
         (left[POSPEECH] == NOUN and 'praMOSentence' in right and right['praMOSentence'] == 'freemember' and right[POSPEECH] == NUMERAL):
         #((left[POSPEECH] in [PRONOUN, ADJECTIVE] and (CATEGORY in left and left[CATEGORY] == POSSESSIVE)) and right[POSPEECH] in [PRONOUN, ADJECTIVE]):
    #if (CASE in left and CASE in right) and left[CASE] == right[CASE]:
        if (CASE in right and right[CASE] == 'accusative') and (CASE in left and left[CASE] != 'accusative'):
            sentence.delByStep(jump_step=0)
            return

        # устанавливаем однородность
        sentence.addHomogeneous(-1, 1) # для дополнений
        sentence.delByStep() # удаляем союз
    #elif left[POSPEECH] == NOUN and right[POSPEECH] == PREPOSITION:
    # Однородности нужны лишь для дополнения связей. В коверторе должны фигурировать лишь связи, но не однородности!


def mark_freemembers(sentence, words):
    for word in words:
        word['praMOSentence'] = 'freemember'
    #sentence.addHomogeneous(*words) # не совсем корректно
    #sentence.jumpByStep(-len(words))


def process_definition(word, sentence, words=None):
    if words is None:
        words = []

    if word[POSPEECH] == ADJECTIVE or (word[POSPEECH] == PRONOUN and word[CATEGORY] == POSSESSIVE) or word[POSPEECH]==NUMERAL:
        words.append(sentence.getByStep())
        if sentence.isLast():
            mark_freemembers(sentence, words)
            return # завершаем цикл, ибо прилагательные без существительного. Их мы не удаляем, так как они могут следовать после глагола esti

        sentence.jumpByStep()
        process_definition(sentence.getByStep(), sentence, words)
    elif word[POSPEECH] in [NOUN] and words: # если перед существительным стояли прилагательные
        sentence.add_feature(sentence.getByStep(), *words)
        sentence.jumpByStep(-len(words))
    else:
        mark_freemembers(sentence, words)


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

    if checkAdverbBefore(sentence):  # порядок менять не рекомендуется: покажи ОЧЕНЬ СИНИЙ цвет.
        # ПОКАЖИ БЫСТРО синий цвет - а вот здесь необходимо расставлять приоритеты для прилагательных и глаголов.
        # БЫСТРО - относится только к глаголам,
        # ПОКАЖИ ОЧЕНЬ синий цвет - стоит перед словом, к которому относится (глагол, наречие, прил)
        # ХОЧУ ОЧЕНЬ СИЛЬНО ; ХОЧУ ОЧЕНЬ - одно и тоже, но в первом случае
        # ОЧЕНЬ относится к СИЛЬНО, а СИЛЬНО - к глаголу. В овтором случае - ОЧЕНЬ относится к глаголу.
        # то есть, одни наречия для прилагательных, другие - для глаголов.
        sentence.add_feature(word.next_sibling, word)
    elif checkAdverbAfter(sentence):
        sentence.add_feature(word.previous_sibling, word)
        sentence.jumpByStep(-1)
    else:
        old_position = sentence.position
        for _word in sentence:  # "свободноплавающее" нарчие. Добавим его к глаголу.
            if _word[POSPEECH] == VERB:
                sentence.add_feature(_word, word) #EX_ERROR если последний  index2, то возникает интересная рекурсивная ошибка.
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


def numeral2number(words):
    """ Числительное в число """
    glued_numeral = ' '.join([word['word'] for word in words])
    numeral_value = 0
    multiplier = 1
    temp_sum = 0
    words.reverse()
    first_iter = True
    for word in words:
        nv = word['number_value']
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
    words.reverse()
    return numeral_value, glued_numeral


def process_numeral(word, sentence, words=None):
    if words is None:
        words = []

    if word[POSPEECH] == NUMERAL or (word[POSPEECH] == NOUN and DERIVATIVE in word and word[DERIVATIVE] == NUMERAL):
        words.append(sentence.getByStep())
        if not sentence.isLast():
            sentence.jumpByStep()
            process_numeral(sentence.getByStep(), sentence, words)
            return

    if len(words) > 1:
        numeral_value, glued_numeral = numeral2number(words)
        last_numeric = words[-1]
        last_numeric['word'] = glued_numeral
        last_numeric['number_value'] = numeral_value
        last_numeric['base'] = ''
        for word in words[:-1]:
            word.remove(-1)


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
