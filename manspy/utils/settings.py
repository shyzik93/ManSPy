from pathlib import Path

import yaml

from manspy.database.database_sqlite3 import Database
from manspy.storage.fasif.parser import parse

DEFAULT_PATH_MODULES = Path(__file__).resolve().parent.parent.parent


class Settings:
    """Класс, хранящий настройки"""
    supported_languages = ['esperanto']
    database = None
    loggers = []

    def __init__(self, **changed_keys):
        if Settings.database is None:
            Settings.database = Database()

        # TODO: описание настроек вынести в строку документации класса
        self.language = changed_keys.get('language', 'esperanto')
        self.history = changed_keys.get('history', False)
        self.send_to_out = changed_keys.get('send_to_out')  # функция, в котору manspy пишет ответ. Устанавливается Интерфейсом
        self.ifname = changed_keys.get('ifname', '')  # уникальное имя интерфейса. Необходимо для журналов.

        # не рекомендуемые к изменению
        # 'real' - real answer, 'fake' - fake answer, 'construct' - construct answer
        self.answer_type = changed_keys.get('answer_type', 'fake')


class InitSettings:
    """Класс, инициализирующий настройки"""
    _IS_ENTERED = False

    def __enter__(self):
        if self._IS_ENTERED:
            raise Exception('You should init `InitSettings` only one!')

        self._IS_ENTERED = True
        with open(DEFAULT_PATH_MODULES / 'manspy/data/relations.yaml', encoding='utf-8') as relations_file:
            for relation_dict in yaml.safe_load(relations_file):
                if relation_dict['count_members'] == 'INFINITY':
                    relation_dict['count_members'] = 0

                Settings.database.add_descr_relation(**relation_dict)

        parse(DEFAULT_PATH_MODULES / 'manspy/data/fasif-verb.yaml', Settings(history=False))
        parse(DEFAULT_PATH_MODULES / 'manspy/data/fasif-word_combination.yaml', Settings(history=False))

    def __exit__(self, Type, Value, Trace):
        for module in Settings.loggers:
            module.close()

        Settings.database.close()
        Settings.database = None

        if Type is None:  # Если исключение не возникло
            pass
        else:             # Если возникло исключение
            return False  # False - исключение не обработано
                          # True  - исключение обработано
