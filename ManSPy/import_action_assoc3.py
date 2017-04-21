# -*- coding: utf-8 -*-
import os, sys, re, json, hashlib
from pprint import pprint
from . import analyse_text, Action, relation, to_formule

NAME_LANG = r'[A-Z][a-z]+'
WORD = r'[a-zа-яёĉĝĥĵŝŭ]+'
WORD_WITH_PREPOSITION = '(?:'+WORD+')?[ \t]*'+WORD

NAME_PYTHON_OBJ = r'[_a-zA-Z][_0-9a-zA-Z]*'
NAME_INTERNAL_OBJ = r'\$'+NAME_PYTHON_OBJ
PATH_FUNCTION = NAME_PYTHON_OBJ+'/'+NAME_PYTHON_OBJ
ALL_NAMES_FUNCTION = r'(?:'+PATH_FUNCTION+'|'+NAME_INTERNAL_OBJ+')'

# Парсинг Verbs
STRING_VERBS_TITLE = r'^'+ALL_NAMES_FUNCTION+'$'
#STRING_VERBS_BODY = r'^ {4}'+NAME_LANG+'[ \t]*:[ \t]*'+WORD_WITH_PREPOSITION+'[ \t]*$'
STRING_VERBS_BODY = r'^ {4}('+NAME_LANG+')[ \t]*:[ \t]*('+WORD_WITH_PREPOSITION+'(?:[ \t]*,[ \t]*'+WORD_WITH_PREPOSITION+')*)[ \t]*$'

STRING_VERBS_TITLE2 = r'^('+ALL_NAMES_FUNCTION+')$'
#STRING_VERBS_BODY2 = r'^ {4}('+NAME_LANG+')[ \t]*:[ \t]*('+WORD_WITH_PREPOSITION+')[ \t]*$'

# Парсинг WordCombination

STRING_DESTINATION_TITLE = r'^[_a-zA-Z0-9]+[ \t]*:[ \t]*'+PATH_FUNCTION+'[ \t]*$'
STRING_DESTINATION_BODY =  r'^ {4}'+NAME_LANG+'[ \t]*:[ \t]*'+WORD+'[ \t]*$'
STRING_ARGUMENT_TITLE1 = r'^'+NAME_PYTHON_OBJ+'[ \t]+[yn][l]?[ \t]*(;[ \t]*'+NAME_LANG+'[ \t]*)+$'
STRING_ARGUMENT_BODY = r'^ {4}[-_+a-zA-Z0-9а-яА-ЯёЁ]+[ \t]*(;[ \t]*('+WORD+')?[ \t]*)+$'
STRING_ARGUMENT_TITLE2 = r'^'+NAME_PYTHON_OBJ+'[ \t]+[yn][l]?[ \t]*$'
STRING_WCOMB_TITLE = r'^'+NAME_LANG+'$'
#STRING_WCOMB_ARGWORD = r'^ {4}'+WORD_WITH_PREPOSITION+'[ \t]*:[ \t]*'+WORD+'[ \t]*(,[ \t]*'+WORD+'[ \t]*)*$' # первое слово - предлог (иногда нужен)
STRING_WCOMB_ARGWORD = r'^ {4}('+WORD_WITH_PREPOSITION+'[ \t]*:[ \t]*'+WORD+'[ \t]*(,[ \t]*'+WORD+'[ \t]*)*;*)+$' # первое слово - предлог (иногда нужен)
STRING_WCOMB = r'^ {4}('+WORD+')?([ \t]+'+WORD+')*[ \t]*$' # Не должо совпадать с названием языка!

not_to_db = ['nombr', 'cifer']

def get_fasif_files(modules_path):
    ''' Функция возвращает мимена МУ '''
    names = os.listdir(modules_path)
    #names [name for name in names if name[-4:]=='.fsf'] # короче, но требует дополнительную память

    x = 0 # длинее, но требует меньше памяти. Вероятно, медленней работаейт. Необходим замер времени
    while x < len(names):
        if names[x][-4:] != '.fsf': del names[x]
        else: x += 1
    return names

def separate_fasifs(fasif):
    fasif = re.sub(r"#[^:].*", '', fasif) # комментарии с середины строки
    #print fasif
    fasif = fasif.split('\n')
    version = fasif.pop(0) # для будущей совместимости версий, возможно.
    dict_assoc_types = {}
    assoc_type = None
    for string in fasif:
        string = string.rstrip()
        if not string: continue
        if len(string) > 2 and string[:2] == '#:':
            assoc_type = string[2:]
            if assoc_type not in dict_assoc_types: dict_assoc_types[assoc_type] = []
            dict_assoc_types[assoc_type].append([])
            continue
        dict_assoc_types[assoc_type][-1].append(string)
    #pprint.pprint(dict_assoc_types)
    return dict_assoc_types

class _FASIF:

    def __init__(self, LangClass):
        self.LangClass = LangClass

    def get_dword(self, word, settings): return list(self.LangClass.NL2IL(word, ':postmorph', settings)(0).getUnit('dict').values())[0]

    def proccess_argword(self, argwords, settings):
        argwords['name'] = self.get_dword(argwords['name'], settings)
        for index, argword in enumerate(argwords['hyperonyms']):
            argwords['hyperonyms'][index] = self.get_dword(argword, settings)


class FASIF_Verb(_FASIF):

    def parse(self, _fasif):
        function = None
        verbs = {}
        for string in _fasif:
            if re.findall(STRING_VERBS_TITLE, string):
                function = re.findall(STRING_VERBS_TITLE2, string)[0]#string.strip()
            elif re.findall(STRING_VERBS_BODY, string):
                lang, verb = re.findall(STRING_VERBS_BODY, string)[0]#string.split(':')
                verbs[lang.strip()] = verb.strip().split()
        return {'function': function, 'verbs': verbs}

    def siftout(self, fasif, lang):
        verbs = fasif['verbs']
        if lang not in verbs: return None
        fasif['verbs'] = verbs[lang]
        return fasif


    def proccess_lingvo_data(self, fasif, OR, fdb, settings):
        words = [self.get_dword(word_verb, settings)['base'] for word_verb in fasif['verbs']]
        id_group = OR.setRelation('synonym', *words) # функция должна возвратить группу, если добавлен хотя бы один синоним
        fasif['verbs'] = id_group # если идентификатор группы отсутсвует (None), то фасиф считается недействительным и не добавляется в базу (игнорируется)
        return fasif

class FASIF_WordCombination(_FASIF):

    def parse(self, _fasif): # подформат состоит из трёх блоков: описание функций, аргументов и словосочетания. Аргументы одинаковы для всех функций
        functions = {}
        args = {}
        wcomb = {}

        ## Блок функций
        destination = None
        ## Блок аргументов
        arg_name = None
        lang_indexes = []
        ## Блок словосочетаний
        lang = None

        arg_indexes = []
        arg_index = 0

        for string in _fasif:
            ## Блок функций
            # Назначение: Модуль/Функция
            if re.findall(STRING_DESTINATION_TITLE, string): # "Name_01 : moduleName/funcName "
                destination, function = string.split(':')
                functions[destination.strip()] = {'function': function.strip(), 'verbs': {}}
                #print '1 $$$$', string
            # Язык: глаголДляФункции
            elif re.findall(STRING_DESTINATION_BODY, string): # "    Language : verbглагол"
                lang, verb = string.split(':')
                functions[destination]['verbs'][lang.strip()] = verb.strip().split()
                #print '2 $$$$', string
            ## Блок аргументов
            # аргумент yORn ; Язык1 ; Язык2
            elif re.findall(STRING_ARGUMENT_TITLE1, string):
                string = string.split(';')
                arg_name, isreq = string.pop(0).split()

                if len(isreq)==2:
                    args_as_list = isreq[1]
                    isreq = isreq[0]
                else: args_as_list = None

                lang_indexes = []
                args[arg_name] = {'isreq': isreq, 'args_as_list': args_as_list, 'argtable': {}, 'argwords': {}}
                for lang in string:
                    args[arg_name]['argtable'][lang.strip()] = {}
                    lang_indexes.append(lang.strip())

                arg_indexes.append(arg_name)
                #print '3 $$$$', string
            elif re.findall(STRING_ARGUMENT_TITLE2, string):
                arg_name, isreq = string.split()

                if len(isreq)==2:
                    args_as_list = isreq[1]
                    isreq = isreq[0]
                else: args_as_list = None

                args[arg_name] = {'isreq': isreq, 'args_as_list': args_as_list, 'argtable': {}, 'argwords': {}}
                arg_indexes.append(arg_name)
                #print '3 $$$$', string
            # Аргумент ; АргументноеСловоНаЯзыке1 ; АргументноеСловоНаЯзыке2
            elif re.findall(STRING_ARGUMENT_BODY, string):
                string = string.strip().split(';')
                arg_value = string.pop(0).strip()
                for index, word in enumerate(string):
                    word = word.strip()
                    if not word: continue
                    args[arg_name]['argtable'][lang_indexes[index]][word] = arg_value
                #print '4 $$$$', string
            elif re.findall(STRING_ARGUMENT_TITLE2, string):
                arg_name, isreq = string.split()
                args[arg_name] = {'isreq': isreq, 'argtable': {}, 'argwords': {}}
                arg_indexes.append(arg_name)
            ## Блок словосочетаний
            # Язык
            elif re.findall(STRING_WCOMB_TITLE, string):
                lang = string.strip()
                for arg_name in args:
                    args[arg_name]['argwords'][lang] = {'in_wcomb': {'name': None, 'hyperonyms': []}, 'another': []}
                arg_index = 0
                #print '5 $$$$', string
            # АргументноеСлово: АбстрактнаяГруппа1, АбстрактнаяГруппа2     Необходимо заменитиь на: # АргументноеСлово: ВходитАбстрГруппа1, ВходитАбстрГруппа2; НеВХодитАбстрГрупп, НеВХодитАбстрГрупп
            elif re.findall(STRING_WCOMB_ARGWORD, string):
                arg_words = string.strip().split(';')
                #print arg_index, string
                arg_word, hyperonyms = arg_words.pop(0).split(':')
                args[arg_indexes[arg_index]]['argwords'][lang]['in_wcomb']['name'] = arg_word
                for hyperonym in hyperonyms.split(','):
                    args[arg_indexes[arg_index]]['argwords'][lang]['in_wcomb']['hyperonyms'].append(hyperonym.strip())

                for _arg_word in arg_words:
                    arg_word, hyperonyms = _arg_word.split(':')
                    args[arg_indexes[arg_index]]['argwords'][lang]['another']['name'] = arg_word
                    for hyperonym in hyperonyms.split(','):
                        args[arg_indexes[arg_index]]['argwords'][lang]['another']['hyperonyms'].append(hyperonym.strip())
                arg_index += 1
                #print '6 $$$$', string
            elif re.findall(STRING_WCOMB, string):
                  wcomb[lang] = string.strip()
        return {'functions': functions, 'wcomb': wcomb, 'args': args}

    def siftout(self, fasif, lang):
        args = {}
        for arg_name, _args in fasif['args'].items():
            argtable = _args['argtable']
            if lang in argtable: _args['argtable'] = argtable[lang]
            elif not argtable: _args['argtable'] = {}
            else: return None
            argwords = _args['argwords']
            if lang in argwords: _args['argwords'] = argwords[lang]
            else: return None

        for destination, value in fasif['functions'].items():
            if lang in value['verbs']: value['verbs'] = value['verbs'][lang]
            else: value['verbs'] = []

        if lang in fasif['wcomb']: fasif['wcomb'] = fasif['wcomb'][lang]
        else: return None

        return fasif

    def proccess_lingvo_data(self, fasif, OR, fdb, settings):
        for arg_name, data in fasif['args'].items():
            _data = data['argtable'].copy().items()
            for arg_word, argtable in _data:
                del data['argtable'][arg_word]
                arg_word = self.get_dword(arg_word, settings)['base']
                data['argtable'][arg_word] = argtable

            self.proccess_argword(data['argwords']['in_wcomb'], settings)
            for argword in data['argwords']['another']:
                self.proccess_argword(argword, settings)

        for destination, value in fasif['functions'].items():
            for index, word_verb in enumerate(value['verbs']):
                value['verbs'][index] = OR.setRelation('synonym', self.get_dword(word_verb, settings)['base'])

        #print '----------------- to formule start'
        wcomb = self.LangClass.NL2IL(fasif['wcomb'], ':synt', settings)(0)
        fasif['argdescr'] = {}
        for argname, data in fasif['args'].items():
            argword = data['argwords']['in_wcomb']['name']
            wcomb.chmanyByValues({'argname':argname}, setstring='subiv:noignore', base=argword['base'], case=argword['case'])
            fasif['argdescr'][argname] = {'isreq':data['isreq'], 'args_as_list':data['args_as_list'], 'argtable':data['argtable'], 'argwords_another':data['argwords']['another'], 'hyperonyms':data['argwords']['in_wcomb']['hyperonyms']}
        del fasif['args']

        fasif['wcomb'] = wcomb.getUnit('dict')
        for argname, data in fasif['argdescr'].items():
            data['isreq'] = True if data['isreq'] == 'y' else False
            for hyperonym in data['hyperonyms']:
                argword = [argword for argword in wcomb.getByValues(setstring='subiv:noignore', argname=argname)][0]
                #print argname, argword
                if argword[1]: base = argword[1]['base']
                else: base = argword[2][0]['base']
                bases = data['argtable'].keys()
                if hyperonym['base'] not in not_to_db: OR.setRelation('hyperonym', hyperonym['base'], base, *bases)#OR.addWordsInAbstractGroup(hyperonym['base'], base, *bases)

        #pprint(fasif['args']) 
        #fwcomb = to_formule.to_formule(fasif['wcomb'], True, fasif['args'])
        #pprint(fwcomb)
        #fdb.add_hashWComb(fwcomb, {'bl':4}, sentence.getUnit('str')['fwords'], '')

        #print '----------------- to formule end'

        return fasif


class ImportAction():
    def __init__(self, LangClass):
        #self.settings = settings
        #self.OR = relation.ObjRelation(settings, settings['storage_version'])
        self.LangClass = LangClass#analyse_text.LangClass()
        #self.fdb = to_formule.FasifDB(settings)

        self.fasif_dir = os.path.join(os.path.dirname(__file__), 'Action')

    def selector_of_function(self, dict_assoc_types, _func_name, *func_args):
        for assoc_type, fasifs in dict_assoc_types.items():

            #func_name = _func_name+assoc_type
            #if func_name not in globals(): continue
            cls_name = 'FASIF_' + assoc_type
            if cls_name not in dir(self):
                if cls_name not in globals(): continue
                self.__setattr__(cls_name, globals()[cls_name](self.LangClass))
            cls = self.__getattribute__(cls_name)

            index = 0
            while index < len(fasifs):
                fasif = fasifs[index]

                new_fasif = object.__getattribute__(cls, _func_name)(fasif, *func_args) #globals()[func_name](fasif, *func_args)
                if not new_fasif: del dict_assoc_types[assoc_type][index]
                else:
                    dict_assoc_types[assoc_type][index] = new_fasif
                    index += 1

        return dict_assoc_types

    def fsf2json(self):
        # fasif_files = get_fasif_files(self.fasif_dir)
 
        # fasif_json_dir = os.path.join(self.fasif_dir, 'fsf2json')
        # if not os.path.exists(fasif_json_dir): os.mkdir(fasif_json_dir)
 
        # for fasif_file in fasif_files:
        #     with open(os.path.join(self.fasif_dir, fasif_file)) as f: fasif = f.read()
        #     # Отделяем ФАСИФы друг от друга
        #     dict_assoc_types = separate_fasifs(fasif)
        #     # Превращаем текст ФАСИФов в словарь
        #     dict_assoc_types = selector_of_function(dict_assoc_types, 'parse')

        #     for assoc_type, fasifs in dict_assoc_types.items():
        #         for fasif in fasifs:
        #             #with open(os.path.join(fasif_json_dir, hashlib.md5(str(fasif)).hexdigest()+'.json'), 'w') as f: json.dump(fasif, f)
        #             with open(os.path.join(fasif_json_dir, hashlib.md5(str(fasif).encode('utf-8')).hexdigest()+'.json'), 'w') as f: json.dump(fasif, f)
        pass


    def proccess(self, fasif_file, fasif_dir, settings):
        ''' Импортирует МД, извлекает и преобразует ФАСИФ  словарь. '''
        #list_FASIF = Action.getObject(module_name, 'list_FASIF')
        with open(os.path.join(fasif_dir, fasif_file)) as f: fasif = f.read()
        # Отделяем ФАСИФы друг от друга
        dict_assoc_types = separate_fasifs(fasif)
        # Превращаем текст ФАСИФов в словарь
        dict_assoc_types = self.selector_of_function(dict_assoc_types, 'parse')
        # Отсеиваем ненужные языки
        dict_assoc_types = self.selector_of_function(dict_assoc_types, 'siftout', settings['language'])
        # Обрабатываем лингвистическую информацию
        dict_assoc_types = self.selector_of_function(dict_assoc_types, 'proccess_lingvo_data', self.OR, self.fdb, settings)

        for assoc_type, fasifs in dict_assoc_types.items():
            for fasif in fasifs: self.fdb.safeFASIF(assoc_type, fasif)

        #pprint(dict_assoc_types)


    def import_for_lang(self, settings):
        self.OR = relation.ObjRelation(settings, settings['storage_version'])
        self.fdb = to_formule.FasifDB(settings)

        fasif_files = get_fasif_files(self.fasif_dir)
        for fasif_file in fasif_files: self.proccess(fasif_file, self.fasif_dir, settings)
