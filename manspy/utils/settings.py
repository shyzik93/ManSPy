import os

from manspy.database.database_sqlite3 import Database
from manspy.storage.fasif.parser import fasif_parser

DEFAULT_PATH_MODULES = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


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
        fasif_parser(os.path.join(DEFAULT_PATH_MODULES, 'manspy/action/'), Settings(history=False))

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
