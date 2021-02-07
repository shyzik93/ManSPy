import re
import os

from manspy.fasif.parser_fasif import FASIF
from manspy.fasif.constants import *


class FASIF_Verb(FASIF):
    def parse(self, _fasif, path_import, settings):
        function = None
        verbs = {}
        for string in _fasif:
            if re.findall(STRING_VERBS_TITLE, string):
                function = re.findall(STRING_VERBS_TITLE2, string)[0]  # string.strip()
                function = os.path.join(path_import, function)
            elif re.findall(STRING_VERBS_BODY, string):
                language, verb = re.findall(STRING_VERBS_BODY, string)[0]  # string.split(':')
                language = language.strip().lower()
                if language in settings.modules['language']:
                    verbs[language] = verb.strip().split()
        return {'function': function, 'verbs': verbs}

    def proccess_lingvo_data(self, fasif, OR, fdb, settings):
        for language, verbs in fasif['verbs'].items():
            words = [self.get_dword(word_verb, settings)['base'] for word_verb in verbs]
            id_group = OR.setRelation('synonym', *words)  # функция должна возвратить группу, если добавлен хотя бы один синоним
            fasif['verbs'][language] = id_group  # TODO: если идентификатор группы отсутсвует (None), то фасиф считается недействительным и не добавляется в базу (игнорируется)
        return fasif
