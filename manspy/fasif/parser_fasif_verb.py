import re
import os

from manspy.fasif.parser_fasif import FASIF
from manspy.fasif.constants import *


class FASIF_Verb(FASIF):
    def parse(self, _fasif, path_import, settings):
        if not isinstance(_fasif, dict):
            return

        if 'functions' in _fasif:
            return

        _fasif['function'] = os.path.join(path_import, _fasif['function'])
        return _fasif

    def proccess_lingvo_data(self, fasif, OR, fdb, settings):
        for language, verbs in fasif['verbs'].items():
            if language in settings.modules['language']:
                words = [self.get_dword(word_verb, settings)['base'] for word_verb in verbs]
                id_group = OR.setRelation('synonym', *words)  # функция должна возвратить группу, если добавлен хотя бы один синоним
                fasif['verbs'][language] = id_group  # TODO: если идентификатор группы отсутсвует (None), то фасиф считается недействительным и не добавляется в базу (игнорируется)
            else:
                fasif['verbs'][language] = None
        return fasif
