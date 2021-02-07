"""
Задача модуля - выдать все совпадения актантов с фасифами. Уточнение фасифа должно происходить в модуле конвертации.
Созранение:
1. Парсится ФАСИФ.
2. В БД сохраняется ФАСИФ и его тип.

Конвертация:
1. Предложение декомпозируется на сказуемое (предикат) и его актанты. Среди актантов могут быть однородные актанты.
2. Для каждого актанта определяется ФАСИФ WCombination-типа.
3. Выделяем аргументные слова из актанта и строим словарь аргументов.
4. Если в предложении употреблён общий глагол, то аргументы передаются в функцию запроса статуса, а результат - в функцию общего глагола.
   Иначе, аргументы подаются в функцию употреблённого глагола.

Определение ФАСИФа определяется через проверку соответветсвия актанта актанту, указанного в ФАСИФе. Алгоритм проверки соответствия:
1. Проверяется каждое словосочетание актанта:
  1. Если дополнение - это константа, то производим точное сравенение с первым дополнение актанта в ФАСИФе.
     Иначе - точная проверка кроме корня. Корень проверяем на вхождение в требуемые гиперонимы.
  2. Для определений - так же.

На четвёртом шаге перед выполнением функций необходио сформировать внутренний язык. Функции выполнятся в модуле логики.
"""
import json
from manspy.unit import Sentence


def compare_fasif_Verb(fasif, verb_base, finded_args, language):
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
    if word['MOSentence'] in ['direct supplement', 'supplement', 'subject']:
        if argworddescr['POSpeech'] != word['POSpeech']:
            if not (argworddescr['POSpeech'] == 'numeral' and word['derivative'] == 'numeral' and word['POSpeech'] in ['noun']):
                return False
        elif not (not argument.getControl(index) or argworddescr['case'] == word['case']):
            return False # для первого дополнения падеж не учитывается
    elif word['MOSentence'] in ['definition', 'circumstance']:
        if argworddescr['POSpeech'] != word['POSpeech']:
            return False # для первого дополнения падеж не учитывается
    else:
        return False
    #flog.write(u'Example: "%s". Found: "%s"\n' % (argworddescr['base'], word['base']))
    if 'argname' not in argworddescr:  # если константное слово
        #flog.write(u'    type: constant word\n')
        if argworddescr['base'] != word['base']:
            return False
    else:
        #flog.write('    type: argument word\n    argname: "%s".\n' % argworddescr['argname'])
        if argworddescr['argname'] not in finded_args: finded_args[argworddescr['argname']] = []
        if 'number_value' in word: argvalue = word['number_value']
        else: argvalue = word['base']
        finded_args[argworddescr['argname']].append(argvalue)  # TODO: #UNIQ_ARGS Нужны ли нам дубли аргументов?
    return True


def jumpToObient(sentence, indexWord, indexObient):
    indexes = sentence.getObient(indexWord)
    if indexes:
        sentence.jumpByIndex(indexes[indexObient])
        sentence.jumpByStep(-1)
    return True if indexes else False


def compare_fasif_WordCombination(fasif, argument, finded_args, language):
    _argument = Sentence(fasif['wcomb'][language])
    first_index = _argument.getIndexesOfFirstWords()
    if first_index: first_index = first_index[0] # однородные слова должны обработаться в следующем цикле
    _argument_iter = Sentence(fasif['wcomb'][language]).iterFromByIndex(first_index)

    first_index = argument.getIndexesOfFirstWords()
    if first_index: first_index = first_index[0] # однородные слова должны обработаться в следующем цикле
    else: return False # "закольцованный" актант - на каждое слово ссылается другое слово.
    for index, word in argument.iterFromByIndex(first_index):
        _index, _word = next(_argument_iter)

        # "Проходимся" по дополнениям (прямые, косвенные, а также подлежащие)
        isright = compare_word(word, index, argument, _word, finded_args) # new
        if not isright:
            # Если инородная константа, то проверяем, не пропущен ли необязательный аргумент среди фичей константы.
            req, noreq = count_wordargs(_word, fasif, language)
            #print word['base'], _word['base'], req, noreq
            if (not req and not noreq) or req: # если это константное слово без аргументных слов среди определений или есть обязательные аргументный слова среди определений
                #flog.write('    "%s" is not native between native members. Not native members can only be in the end of sentence.\n' % word['base'])
                return False # если посреди связей чужой член - актант не соответсвует фасифу
            else: # если всен аргументные слова - необязательные, то константа может быть пропущена
                argument.jumpByStep(-1)
                _indexes = jumpToObient(_argument, _index, 0)
                if not _indexes: 
                    #flog.write('    "%s" - has %s obients. \n' % (_word['base'], str(_indexes)))
                    break
        #flog.write('    Result of comparing word is right: index - %i, base - "%s".\n' % (index, word['base']))
        indexes = jumpToObient(argument, index, 0)
        _indexes = jumpToObient(_argument, _index, 0)
        # "Проходимся" по обстоятельствам и определениям
        features = word['feature']
        _features = _word['feature']
        for feature in features:
            for _feature in _features:
                isright = compare_word(feature, index, argument, _feature, finded_args)
                #flog.write('    Result of comparing word is %s: index - %i, base - "%s".\n' % (str(isright), index, word['base']))
                # не проверяем на верность.

        # "Проходимся" по однородным дополнениям (прямые, косвенные, а также подлежащие), если это не первый член
  
        # игнорируем лишние косвенные дополнения (на хвосте)
        if not (indexes and _indexes):
            break

    return True


class FasifDB:
    def __init__(self, c, cu):
        self.c, self.cu = c, cu
        self.cu.execute('''
            CREATE TABLE IF NOT EXISTS fasifs (
                id_fasif INTEGER PRIMARY KEY AUTOINCREMENT,
                type_fasif TEXT,
                fasif TEXT UNIQUE ON CONFLICT IGNORE
        );''')

    def safe(self, type_fasif, fasif):
        self.cu.execute(
            'INSERT INTO fasifs (type_fasif, fasif) VALUES (?,?)',
            (type_fasif, json.dumps(fasif, sort_keys=True))
        )
        self.c.commit()

    def find(self, type_fasif, argument, language='esperanto'):
        compared_fasifs = []
        rows = self.cu.execute('SELECT fasif FROM fasifs WHERE type_fasif=?', (type_fasif,))
        for row in rows:
            fasif = json.loads(row['fasif'])
            finded_args = {}
            isright = False
            if type_fasif == 'WordCombination':
                isright = compare_fasif_WordCombination(fasif, argument, finded_args, language)
            elif type_fasif == 'Verb':
                isright = compare_fasif_Verb(fasif, argument, finded_args, language)

            if isright:
                compared_fasifs.append([finded_args, fasif])

        return compared_fasifs
