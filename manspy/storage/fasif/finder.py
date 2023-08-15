"""
Задача модуля - выдать все совпадения актантов с фасифами. Уточнение фасифа должно происходить в модуле конвертации.
Созранение:
1. Парсится ФАСИФ.
2. В БД сохраняется ФАСИФ и его тип.

Конвертация:
1. Предложение декомпозируется на сказуемое (предикат) и его актанты. Среди актантов могут быть однородные актанты.
2. Для каждого актанта определяется ФАСИФ WCombination-типа.
3. Выделяем аргументные слова из актанта и строим словарь аргументов.
4. Если в предложении употреблён общий глагол, то аргументы передаются в функцию запроса статуса,
   а результат - в функцию общего глагола.
   Иначе, аргументы подаются в функцию употреблённого глагола.

Определение ФАСИФа определяется через проверку соответветсвия актанта актанту, указанного в ФАСИФе.
Алгоритм проверки соответствия:
1. Проверяется каждое словосочетание актанта:
  1. Если дополнение - это константа, то производим точное сравенение с первым дополнение актанта в ФАСИФе.
     Иначе - точная проверка кроме корня. Корень проверяем на вхождение в требуемые гиперонимы.
  2. Для определений - так же.

На четвёртом шаге перед выполнением функций необходио сформировать внутренний язык. Функции выполнятся в модуле логики.
"""
from manspy.utils.constants import (
    CASE, CIRCUMSTANCE,
    DEFINITION, DERIVATIVE, DIRECT_SUPPLEMENT,
    MOSENTENCE,
    NOUN, NUMERAL,
    POSPEECH,
    SUBJECT, SUPPLEMENT,
)
from manspy.utils.unit import Sentence


def compare_fasif_verb(fasif, verb_base, finded_args, language):
    if verb_base != fasif['verbs'][language]:
        return False
    finded_args[0] = fasif['function']
    return True


def count_wordargs(constwordexample, fasif, language):
    req = noreq = 0
    for feature in constwordexample['feature']:
        if 'argname' in feature:
            if fasif['argdescr'][language][feature['argname']]['isreq']:
                req += 1
            else:
                noreq += 1

    return req, noreq


def compare_word(word, index, argument, argworddescr, finded_args):
    if word[MOSENTENCE] in [DIRECT_SUPPLEMENT, SUPPLEMENT, SUBJECT]:
        if argworddescr[POSPEECH] != word[POSPEECH]:
            if not (argworddescr[POSPEECH] == NUMERAL and word[DERIVATIVE] == NUMERAL and word[POSPEECH] in [NOUN]):
                return False
        elif not (not argument.getControl(index) or argworddescr[CASE] == word[CASE]):
            return False  # для первого дополнения падеж не учитывается
    elif word[MOSENTENCE] in [DEFINITION, CIRCUMSTANCE]:
        if argworddescr[POSPEECH] != word[POSPEECH]:
            return False  # для первого дополнения падеж не учитывается
    else:
        return False
    # flog.write(u'Example: "%s". Found: "%s"\n' % (argworddescr['base'], word['base']))
    if 'argname' not in argworddescr:  # если константное слово
        # flog.write(u'    type: constant word\n')
        if argworddescr['base'] != word['base']:
            return False
    else:
        # flog.write('    type: argument word\n    argname: "%s".\n' % argworddescr['argname'])
        if argworddescr['argname'] not in finded_args:
            finded_args[argworddescr['argname']] = []
        if 'number_value' in word:
            argvalue = word['number_value']
        else:
            argvalue = word['base']
        finded_args[argworddescr['argname']].append(argvalue)  # TODO: #UNIQ_ARGS Нужны ли нам дубли аргументов?
    return True


def jump_to_obient(sentence, index_word, index_obient):
    indexes = sentence.getObient(index_word)
    if indexes:
        sentence.jumpByIndex(indexes[index_obient])
        sentence.jumpByStep(-1)
    return True if indexes else False


def compare_fasif_word_combination(fasif, argument, finded_args, language):
    _argument = Sentence(None, imports=fasif['wcomb'][language])
    first_words = _argument.get_indexes_of_first_words()
    if first_words:
        first_word = first_words[0]  # однородные слова должны обработаться в следующем цикле

    _argument_iter = Sentence(None, imports=fasif['wcomb'][language]).iterFromByIndex(first_word.index)

    first_words = argument.get_indexes_of_first_words()
    if first_words:
        first_word = first_words[0]  # однородные слова должны обработаться в следующем цикле
    else:
        return False  # "закольцованный" актант - на каждое слово ссылается другое слово.

    for word in argument.iterFromByIndex(first_word.index):
        _word = next(_argument_iter)

        # "Проходимся" по дополнениям (прямые, косвенные, а также подлежащие)
        isright = compare_word(word, word.index, argument, _word, finded_args)  # new
        if not isright:
            # Если инородная константа, то проверяем, не пропущен ли необязательный аргумент среди фичей константы.
            req, noreq = count_wordargs(_word, fasif, language)
            # print word['base'], _word['base'], req, noreq
            if (not req and not noreq) or req:  # если это константное слово без аргументных слов среди определений или есть обязательные аргументный слова среди определений
                # flog.write('    "%s" is not native between native members. Not native members can only be in the end of sentence.\n' % word['base'])
                return False  # если посреди связей чужой член - актант не соответсвует фасифу
            else:  # если всен аргументные слова - необязательные, то константа может быть пропущена
                argument.jumpByStep(-1)
                _indexes = jump_to_obient(_argument, _word['index'], 0)
                if not _indexes: 
                    # flog.write('    "%s" - has %s obients. \n' % (_word['base'], str(_indexes)))
                    break

        # flog.write('    Result of comparing word is right: index - %i, base - "%s".\n' % (index, word['base']))
        indexes = jump_to_obient(argument, word.index, 0)
        _indexes = jump_to_obient(_argument, _word['index'], 0)
        # "Проходимся" по обстоятельствам и определениям
        features = word['feature']
        _features = _word['feature']
        for feature in features:
            for _feature in _features:
                isright = compare_word(feature, word.index, argument, _feature, finded_args)
                # flog.write('    Result of comparing word is %s: index - %i, base - "%s".\n' % (str(isright), index, word['base']))
                # не проверяем на верность.

        # "Проходимся" по однородным дополнениям (прямые, косвенные, а также подлежащие), если это не первый член
  
        # игнорируем лишние косвенные дополнения (на хвосте)
        if not (indexes and _indexes):
            break

    return True


def find(settings, type_fasif, argument, language='esperanto'):
    compared_fasifs = []
    for fasif in settings.database.get_fasif(type_fasif):
        finded_args = {}
        compare_fasif = globals()[f'compare_fasif_{type_fasif}']
        if compare_fasif(fasif, argument, finded_args, language):
            compared_fasifs.append([finded_args, fasif])

    return compared_fasifs
