"""
    https://mw.lojban.org/index.php?title=%D0%92%D0%BE%D0%BB%D0%BD%D1%8B_%D0%9B%D0%BE%D0%B6%D0%B1%D0%B0%D0%BD%D0%B0#.D0.92.D0.BE.D0.BB.D0.BD.D0.B0_2_.28FA_.D0.B8_zo.27e.29
"""
import re
from manspy.utils import unit

vowels_low = "aeiouy"
vowels_up = "AEIOUY"
consonants_low = "bcdfgjklmnprstvxz'"
consonants_up = "BCDFGJKLMNPRSTVXZ'"

all_symbols = {
    "letter": vowels_low + vowels_up + consonants_low + consonants_up,
    "smark": ".," # special marks
    }

# tools 

def define_type_symbol(word, all_symbols):
    for index, symbol in word:
        symbol['type'] = 'other'
        for symbol_name, symbols in all_symbols:
            if symbol['symbol'] in symbols: symbol['type'] = symbol_name


def proccessEndWord(sword, word, symbols):
    for index in range(1, len(sword)):
        if sword[-index] not in symbols: break
        word['end_orig'] += sword[-index]
    word['word'] = sword[:-len(word['end_orig'])]


def getGraphmathA(text):
    # Заменяем символы
    words = text.split()
    words = [unit.Word(word) for word in words]

    for word in words: define_type_symbol(word, all_symbols)

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
        sword = word['word']
        word['end'] = word['end_orig'] = ''
        # слово с пунктуационными символами на конце
        if sword[-1] in '.!?':
            proccessEndWord(sword, word, '.!?')
            if '?' in word['end_orig']: word['end'] = '?'
            elif '!' in word['end_orig']: word['end'] = '!'
            elif '...' in word['end_orig']: word['end'] = '...'
            elif '.' in word['end_orig']: word['end'] = '.'
        elif sword[-1] in ',;:':
            proccessEndWord(sword, word, ',;:')
            word['end'] = word['end_orig'][0]
        # слово с небуквенными символами в середине или начале
        if not word['word'].isalpha():
            if re.match(r'^[0-9]*[,.]?[0-9]+$', sword): word['notword'] = 'figure'

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

    return unit.Text([unit.Sentence(sentence) for sentence in text])
