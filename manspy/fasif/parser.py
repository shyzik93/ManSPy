import os
import re
import json

from manspy.relation import ObjRelation
from manspy.fasif import finder
from manspy.fasif.parser_fasif_verb import FASIF_Verb
from manspy.fasif.parser_fasif_word_combination import FASIF_WordCombination


def remove_comments_and_separate_fasifs(fasif):
    if fasif.startswith("["):
        return {'Verb': json.loads(fasif)}
    fasif = re.sub(r'#[^:].*', '', fasif)
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
    def parse(self, path_import, language, settings):
        OR = ObjRelation(settings.c, settings.cu)
        fdb = finder.FasifDB(settings.c, settings.cu)

        for fasif_file_name in os.listdir(path_import):
            if fasif_file_name.endswith('.fsf') or fasif_file_name.endswith('.json'):
                with open(os.path.join(path_import, fasif_file_name), encoding='utf-8') as fasif_file:
                    # Отделяем ФАСИФы друг от друга
                    dict_assoc_types = remove_comments_and_separate_fasifs(fasif_file.read())
                    for assoc_type, fasifs in dict_assoc_types.items():
                        cls = globals()['FASIF_{}'.format(assoc_type)]()
                        for fasif in fasifs:
                            # Превращаем текст ФАСИФов в словарь
                            fasif = cls.parse(fasif, path_import, settings)
                            if fasif:
                                # Обрабатываем лингвистическую информацию
                                fasif = cls.proccess_lingvo_data(fasif, OR, fdb, settings)
                                if fasif:
                                    fdb.safe(assoc_type, fasif)
