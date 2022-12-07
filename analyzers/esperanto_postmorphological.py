# -*- coding: utf-8 -*-
''' Модуль выполняет расширенный морфологический разбор слова,
    то есть на основе связей в предложении.
    По завершению удаляются все служебные части речи.
    Можно приступать к синтаксичекому анализу предложения.
    '''


def process_article(word, sentence):
    if word['POSpeech'] == 'article':
        sentence.delByStep()  # пока только удаляем


def process_preposition(word, sentence):
    if word['POSpeech'] != 'preposition':
        return

    left, right = sentence.getNeighbours()
    if right is None:
        sentence.delByStep()

    elif right['POSpeech'] in ['noun', 'pronoun', 'numeral']:
        sentence.getByStep(1, 'case', word['give_case'])
        sentence.delByStep()
    else:
        sentence.error.add("postmorph", 'After preposition "'+word['word']+'" must be a noun or a pronoun or a cardinal numeral! Found '+str(sentence.getByStep(1)), 0)


def process_conjunction(word, sentence):
    if word['POSpeech'] != 'conjunction' or word['value'] != 'coordinating':
        return

    left, right = sentence.getNeighbours()
    if left is None or right is None:  # если союз первый или последний в предложении
        sentence.delByStep()

    # сочинительный союз
    #if word['word'] == 'kaj': # заменить логическими символами (kaj = &)
    #print word['base']
    if left['POSpeech'] == right['POSpeech'] or \
         (left['POSpeech'] == 'noun' and right['POSpeech'] == 'pronoun' and right['category'] != 'possessive') or (right['POSpeech'] == 'noun' and left['POSpeech'] == 'pronoun' and left['category'] != 'possessive') or \
         ((left['POSpeech'] == 'pronoun' and left['category'] == 'possessive') and right['POSpeech'] == 'adjective') or ((right['POSpeech'] == 'pronoun' and right['category'] == 'possessive') and left['POSpeech'] == 'adjective') or \
         (left['POSpeech'] == 'noun' and 'praMOSentence' in right and right['praMOSentence'] == 'freemember' and right['POSpeech'] == 'numeral'):
         #((left['POSpeech'] in ['pronoun', 'adjective'] and ('category' in left and left['category'] == 'possessive')) and right['POSpeech'] in ['pronoun', 'adjective']):
    #if ('case' in left and 'case' in right) and left['case'] == right['case']:
        if ('case' in right and right['case'] == 'accusative') and ('case' in left and left['case'] != 'accusative'):
            sentence.delByStep(jump_step=0)
            return

        # устанавливаем однородность
        sentence.addHomogeneous(-1, 1) # для дополнений
        sentence.delByStep() # удаляем союз
    #elif left['POSpeech'] == 'noun' and right['POSpeech'] == 'preposition':
    # Однородности нужны лишь для дополнения связей. В коверторе должны фигурировать лишь связи, но не однородности!


def mark_freemembers(sentence, indexes):
    for index in indexes:
        sentence(index, 'praMOSentence', 'freemember')
    #sentence.addHomogeneous(*indexes) # не совсем корректно
    #sentence.jumpByStep(-len(indexes))


def process_definition(word, sentence, indexes=None):
    if indexes is None:
        indexes = []
    #print 'findDefinition:', word['word'], index, len(sentence.subunit_info)
    if word['POSpeech'] == 'adjective' or (word['POSpeech'] == 'pronoun' and word['category'] == 'possessive') or word['POSpeech']=='numeral':
        indexes.append(sentence.currentIndex())
        if sentence.isLast():
            mark_freemembers(sentence, indexes)
            return # завершаем цикл, ибо прилагательные без существительного. Их мы не удаляем, так как они могут следовать после глагола esti

        sentence.jumpByStep()
        process_definition(sentence.getByStep(), sentence, indexes)
    elif word['POSpeech'] in ['noun'] and indexes: # если перед существительным стояли прилагательные
        sentence.addFeature(sentence.currentIndex(), *indexes)
        sentence.jumpByStep(-len(indexes))
    else:
        mark_freemembers(sentence, indexes)


def checkAdverbBefore(sentence):
    if sentence.position+1 >= len(sentence.subunit_info):
        return False  # т. е. является последним

    # if adverb['base'] == u'ankaŭ': # стоит перед словом, к которому относится
    return sentence.getByStep(1, 'POSpeech') in ['verb', 'adjective', 'adverb']


def checkAdverbAfter(sentence):
    if sentence.isFirst():
        return False

    return sentence.getByStep(-1, 'POSpeech') in ('verb', 'adjective', 'adverb')


def process_adverb(word, sentence):
    if sentence.getByStep()['POSpeech'] != 'adverb':
        return

    index = sentence.currentIndex()
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
            if word['POSpeech'] == 'verb':
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
            if 'case' in word:
                sentence(index_homo, 'case', word['case'])

            done_indexes.append(index_homo)


def numeral2number(sentence, indexes):
    """ Числительное в число """
    glued_numeral = ' '.join([sentence(index, 'word') for index in indexes])
    numeral_value = 0
    multiplier = 1
    temp_sum = 0
    indexes.reverse()
    first_iter = True
    for index in indexes:
        nv = sentence(index, 'number_value')
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

    if word['POSpeech'] == 'numeral' or (word['POSpeech'] == 'noun' and 'derivative' in word and word['derivative'] == 'numeral'):
        indexes.append(sentence.currentIndex())
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
    sentence(indexes[-1], 'word', glued_numeral)
    sentence(indexes[-1], 'number_value', numeral_value)
    sentence(indexes[-1], 'base', '')
    sentence.delByIndex(*indexes[:-1])
    sentence.jumpByStep(-len(indexes))


def get_analysis(text):
    ''' Обёртка '''
    for sentence in text:
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

    return text
