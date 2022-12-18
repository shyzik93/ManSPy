import importlib
import os

from manspy.storage.fasif.parser import fasif_parser


DEFAULT_PATH_MODULES = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DEFAULT_PATHS_IMPORT = [
    ('logger', 'manspy.loggers.logger_db'),
    ('logger', 'manspy.loggers.logger_plain_text'),
    ('database', 'manspy.database.database_sqlite3'),  # модуль базы должен быть перед модулем действий
]


class Settings:
    """Класс, хранящий настройки"""
    languages = ['esperanto']
    paths_import = DEFAULT_PATHS_IMPORT
    modules = {
        'logger': {},
    }
    db_settings = {
        'path': ':memory:',
    }
    database = None
    loggers = []

    def __init__(self, **changed_keys):
        # TODO: описание настроек вынести в строку документации класса
        self.language = changed_keys.get('language', 'esperanto')
        self.history = changed_keys.get('history', False)
        self.send_to_out = changed_keys.get('send_to_out')  # функция, в котору manspy пишет ответ. Устанавливается Интерфейсом
        self.ifname = changed_keys.get('ifname', '')  # уникальное имя интерфейса. Необходимо для журналов.

        # не рекомендуемые к изменению
        # 'real' - real answer, 'fake' - fake answer, 'construct' - construct answer
        self.answer_type = changed_keys.get('answer_type', 'fake')

        paths_import = changed_keys.get('paths_import', [])
        self.paths_import.extend(paths_import)

    @classmethod
    def set_module(cls, module_type, module, module_code):
        cls.modules.setdefault(module_type, {})[module_code] = module


class InitSettings:
    """Класс, инициализирующий настройки"""
    _IS_ENTERED = False

    def __enter__(self):
        if self._IS_ENTERED:
            raise Exception('You should init `InitSettings` only one!')

        self._IS_ENTERED = True
        for module_type, path_import in Settings.paths_import:
            module_obj = importlib.import_module(path_import)
            if module_type == 'database':
                Settings.database = module_obj.Database(Settings.db_settings)
            if module_type == 'logger':
                module = module_obj.Logger()
                Settings.loggers.append(module)

        fasif_parser(os.path.join(DEFAULT_PATH_MODULES, 'manspy/action/'), Settings(history=False))

    def __exit__(self, Type, Value, Trace):
        for module_code, module in Settings.modules['logger'].items():
            module.close()

        Settings.database.close()

        if Type is None:  # Если исключение не возникло
            pass
        else:             # Если возникло исключение
            return False  # False - исключение не обработано
                          # True  - исключение обработано
