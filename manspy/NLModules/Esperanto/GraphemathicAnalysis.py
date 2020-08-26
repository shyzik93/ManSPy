""" Графематический анализ текста.
    Словарь символа: {'symbol': Символ, 'type': 'letter' OR 'punctuation_mark' OR 'other'}
    Словарь слова: {'word': СписокСимволов}
    Задача модуля: выдать предложение, состоящее из слов и неслов. Неслова - это текст в кавычках, имена файлов, адреса и прочее, что может испортить последущие анализы.
    Благодаря чему морфологический модуль будет уже знать, где слово, а где - не слово..
"""
import re
from .. import ObjUnit

low_letters = u"ABCĈDEFGĜHĤIJĴKLMNOPRSŜTUŬVZ"
up_letters =  u"abcĉdefgĝhĥijĵklmnoprsŝtuŭvz"
letters = up_letters + low_letters
punctuation_marks = u".,;:!?-'\""

ReplacedLetters = {u'cx' :u'ĉ', u'gx': u'ĝ', u'hx': u'ĥ',
           u'jx': u'ĵ', u'sx': u'ŝ', u'ux': u'ŭ',
           u'\t': u'', u'\n': u''}

def define_type_symbol(word):
    """ Устанавливаем тип символа в слове """
    for index, symbol in word:
        if symbol['symbol'] in letters: symbol['type'] = 'letter'
        elif symbol['symbol'] in punctuation_marks: symbol['type'] = 'pmark'
        else: symbol['type'] = 'other'

def strip_word_end(word, symbols):
    """ Обрезает сивмолы `symbols` с конца слова"""
    word_stripped = word['word'].rstrip(symbols)
    word['end_orig'] = word['word'][-len(word_stripped):]
    word['word'] = word_stripped

    # OLD_CODE
    # for index in range(1, len(word['word'])):
    #     if word['word'][-index] not in symbols: break
    #     word['end_orig'] += word['word'][-index]
    # word['word'] = word['word'][:-len(word['end_orig'])]

def process_end_of_word(word):
    """ Обработка последних символов в слове (потенциальные пунктуационные знаки) """
    sword = word['word']
    word['end'] = word['end_orig'] = ''
    # слово с пунктуационными символами на конце
    if sword[-1] in '.!?':
        strip_word_end(word, '.!?')
        if '?' in word['end_orig']: word['end'] = '?'
        elif '!' in word['end_orig']: word['end'] = '!'
        elif '...' in word['end_orig']: word['end'] = '...'
        elif '.' in word['end_orig']: word['end'] = '.'
    elif sword[-1] in ',;:':
        strip_word_end(word, ',;:')
        word['end'] = word['end_orig'][0]
    # слово с небуквенными символами в середине или начале
    if not word['word'].isalpha():
        if re.match(r'^[0-9]*[,.]?[0-9]+$', sword): word['notword'] = 'figure'

def getGraphmathA(text):
    # Заменяем символы
    for k, v in ReplacedLetters.items(): text = text.replace(k, v)
    words = text.split()
    words = [ObjUnit.Word(word) for word in words]

    for word in words: define_type_symbol(word)

    # Присоединяем отдельностоящие символы пунктуации к концу слова
    index = 0
    while index < len(words):
        word = words[index]
        sword = word['word']
        if re.match(r'(?:[.]+)|(?:[,]+)|(?:[?!]+)|(?:[:]+)', sword):
            if index: words[index-1]['word'] += sword
            del words[index]
            index -= 1
        index += 1

    # Обработка последних символов в слове (потенциальные пунктуационные знаки)
    for word in words:
        process_end_of_word(word)

    # обработка кавычек вокруг одного слова
    for word in words:
        sword = word['word']
        if sword[-1] == sword[0] and (sword[-1] == '"' or sword[-1] == "'"):
            word['word'] = sword[1:-1]
            word['around_pmark'].append('quota')

    # Разбиваем текст на ВОЗМОЖНЫЕ предложения
    text = []
    sentence = []
    for word in words:
        sentence.append(word)
        if word['end'] in ['.', '...', '!', '?']:
            text.append(sentence)
            sentence = []
    if len(sentence) > 0:
        text.append(sentence)
        #sentence_words['end'] = '.'

    #print len(words), len(sentences)
    #for sentence in sentences:
    #  print len(sentence)#sentence.getUnit('dict')


    # обработка кавычек

    # обработка слов, с небуквенными символами (email, url, file, etc)

    return ObjUnit.Text([ObjUnit.Sentence(sentence) for sentence in text])
