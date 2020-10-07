import os
import re

from manspy import relation
from manspy.fasif import finder
from manspy.fasif.parser_fasif_verb import FASIF_Verb
from manspy.fasif.parser_fasif_word_combination import FASIF_WordCombination


def remove_comments_and_separate_fasifs(fasif):
    fasif = re.sub(r"#[^:].*", '', fasif)
    fasif = fasif.split('\n')
    version = fasif.pop(0)  # для будущей совместимости версий, возможно.
    dict_assoc_types = {}
    assoc_type = None
    for string in fasif:
        string = string.rstrip()
        if not string: continue
        if len(string) > 2 and string[:2] == '#:':
            assoc_type = string[2:]
            if assoc_type not in dict_assoc_types:
                dict_assoc_types[assoc_type] = []
            dict_assoc_types[assoc_type].append([])
            continue
        dict_assoc_types[assoc_type][-1].append(string)
    return dict_assoc_types


class FASIFParser:
    def __init__(self, LangClass):
        self.LangClass = LangClass
        self.classes = {}

    def selector_of_function(self, dict_assoc_types, _func_name, *func_args):
        for assoc_type, fasifs in dict_assoc_types.items():
            cls_name = 'FASIF_' + assoc_type
            if cls_name not in self.classes and cls_name in globals():
                self.classes[cls_name] = globals()[cls_name](self.LangClass)

            index = 0
            while index < len(fasifs):
                new_fasif = getattr(self.classes[cls_name], _func_name)(fasifs[index], *func_args)
                if new_fasif:
                    dict_assoc_types[assoc_type][index] = new_fasif
                    index += 1
                else:
                    del dict_assoc_types[assoc_type][index]

        return dict_assoc_types

    def parse(self, path_import,  language, settings):
        OR = relation.ObjRelation(language, settings.storage_version)
        fdb = finder.FasifDB(language)

        for fasif_file_name in os.listdir(path_import):
            if fasif_file_name.endswith('.fsf'):
                with open(os.path.join(path_import, fasif_file_name), encoding='utf-8') as fasif_file:
                    # Отделяем ФАСИФы друг от друга
                    dict_assoc_types = remove_comments_and_separate_fasifs(fasif_file.read())
                    # Превращаем текст ФАСИФов в словарь
                    dict_assoc_types = self.selector_of_function(dict_assoc_types, 'parse', path_import)
                    # Отсеиваем ненужные языки
                    dict_assoc_types = self.selector_of_function(dict_assoc_types, 'siftout', language)
                    # Обрабатываем лингвистическую информацию
                    dict_assoc_types = self.selector_of_function(dict_assoc_types, 'proccess_lingvo_data', OR, fdb, settings)

                    for assoc_type, fasifs in dict_assoc_types.items():
                        for fasif in fasifs:
                            fdb.safeFASIF(assoc_type, fasif)
