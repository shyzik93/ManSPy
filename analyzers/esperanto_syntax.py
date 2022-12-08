# -*- coding: utf-8 -*-
''' Модуль выполняет синтаксический анализ предложения

  Определяются члены предложения и устанавливаются связи слов.
'''

def forPronounAndNoun(word):
    ''' Определяет член предложения для имени существительного
        и притяжательного местоимепния по падежу '''
    if word['case'] == 'accusative':
        return 'direct supplement'
    elif word['case'] == 'nominative':
        return 'subject'
    return 'supplement'


def setMOS_ToSign(features):
    """ Определение члена предложения у признаков:
        прилагательного, наречия, """
    for feature in features:
        if feature['POSpeech'] == 'adjective' or (feature['POSpeech'] == 'pronoun' and feature['category'] == 'possessive') or feature['POSpeech'] == 'numeral':
            feature['MOSentence'] = 'definition'
        elif feature['POSpeech'] == 'adverb':
            feature['MOSentence'] = 'circumstance'
        if feature['feature']:
            setMOS_ToSign(feature['feature'])


def setMOSentence(word, sentence):
    if word['POSpeech'] == 'verb':
        word['MOSentence'] = 'predicate'
        if word['feature']:
            setMOS_ToSign(word['feature'])

    #ATTENTION обстоятельства, выраженные существительным, определяются в модуле
    # промежуточного анализа как наречие.
    elif word['POSpeech'] == 'noun' or (word['POSpeech'] == 'numeral' and word['class'] == 'cardinal'):
        word['MOSentence'] = forPronounAndNoun(word)
        if word['feature']:
            setMOS_ToSign(word['feature'])

    elif word['POSpeech'] == 'pronoun':
        if word['category'] == 'possessive':
            word['MOSentence'] = 'definition'  # ? Появилось определение
        elif word['category'] == 'personal':
            word['MOSentence'] = forPronounAndNoun(word)
        else:
            word['MOSentence'] = ''  # не притяжательное и не личное местоимение

    # прилагательное без существительного
    elif 'praPOSpeech' in word and word['praMOSentence'] == 'freemember':
        word['MOSentence'] = 'supplement'
    #elif word['POSpeech'] == 'adjective': word['MOSentence'] = 'definition'  
    else:
        word['MOSentence'] = ''


def setLinks(word, sentence):
    ''' Устанавливает связи членов предложения. Обстоятельства и определения
        спрятаны в тех, к кому они относятся. Работаем лишь со сказуемым,
        подлежащим и дополнением. '''
    if word['MOSentence'] == 'predicate':
        # линкуем сказуемое и прямое дополнение
        old_position = sentence.position
        for word2 in sentence.iterFromByStep(1):
            if word2['MOSentence'] == 'direct supplement':
                sentence.addLink(word, word2)
            elif word2['MOSentence'] == 'predicate':
                break

        sentence.position = old_position

    #  TODO: если у прямого дополнения нескеолько дополнений, то они проигнорируются
    elif word['MOSentence'] in ['direct supplement', 'supplement', 'subject']:
        # линкуем прямое дополнение и следующее после него косвенное дополнение
        old_position = sentence.position
        case = None
        for word2 in sentence.iterFromByStep(1):
            if word2['MOSentence'] == 'supplement':# and word2['case'] != "":
                """# остальные падежи, вероятно, будут означать, что косв. дополнение -
                # это обстоятельство, то есть относится к сказуемому.
                #if sentence(index2, 'case') in ['genetive']: sentence.addLink(index, index2)#word['link'].append(index2)"""
                if not case:
                    case = word['case']
                sentence.addLink(word, word2)
            elif word2['MOSentence'] in ['direct supplement', 'subject']:
                break  # это другой актант уже пойдёт.

        sentence.position = old_position


def goThrowLinks(index, sentence, indexes=None):

    if indexes is None:
        indexes = []

    if index not in indexes:
        indexes.append(index)
    
        for index_link in sentence(index, 'link'):
            goThrowLinks(index_link, sentence, indexes)
        for index_link in sentence(index, 'homogeneous_link'):
            goThrowLinks(index_link, sentence, indexes)    

    return indexes


# TODO: Две одноимённых функции!???
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
        if sentence(first_index, 'POSpeech') == 'conjuction':
            conjunctions.append(first_index) # сочинённых союзов между однородными членами должны исчезнуть в предыдущих шагах.
        if sentence(first_index, 'POSentence') == 'subject':
            subjects.append(first_index)
        if sentence(first_index, 'POSentence') == 'predicate':
            predicates.append(first_index)    

    for subject in subjects:
        _sentences.append(goThrowLinks(subject, sentence))

    # определяем, в каком 
    for conjunction in conjunctions:
        sentence.jumpByIndex(conjunction['index'])
        left, right = sentence.getNeighbours()

    #for index, word in sentence:
    #    left, right = sentence.getNeighbours()


def split_sentence(sentence):
    first_indexes = sentence.getIndexesOfFirstWords()
    #first_words = [sentence(i, 'word') for i in first_indexes]
    #print('            Root words of the sentence:', [sentence(i, 'word') for i in first_indexes])

    conjunctions = []
    _sentences = []

    # import json
    # print('FirstIndees:', first_indexes)
    # print('sentence:', json.dumps(sentence.export_unit(), sort_keys=True, indent=4).replace('"', ''))
    for first_index in first_indexes:
        _sentences.append(goThrowLinks(first_index, sentence))    


def analyze(message):
    for sentence in message.text:
        # определяет члены предложения
        for word in sentence:
            setMOSentence(word, sentence)
        # устанавливает связи членов предложения
        for word in sentence:
            setLinks(word, sentence)

        # разделяем сложноподчинённые и сложносочинённые предложения
        split_sentence(sentence)

    return message.text
