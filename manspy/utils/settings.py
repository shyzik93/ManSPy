import os

from manspy.fasif.parser import fasif_parser
from manspy.utils import importer


DEFAULT_PATH_MODULES = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DEFAULT_PATHS_IMPORT = [
    ('language', os.path.join(DEFAULT_PATH_MODULES, 'language')),  # модуль языка должен быть перед модулем действий
    ('logger', os.path.join(DEFAULT_PATH_MODULES, 'logger')),
    ('database', os.path.join(DEFAULT_PATH_MODULES, 'database')),  # модуль базы должен быть перед модулем действий
    ('action', os.path.join(DEFAULT_PATH_MODULES, 'action')),
]


class Settings:
    """Класс, хранящий настройки"""
    paths_import = DEFAULT_PATHS_IMPORT
    modules = {
        'language': {},
        'logger': {},
        'interface': {},
        'database': {},
    }
    db_type = 'sqlite3'
    db_settings = {
        'sqlite3': {
            'path': ':memory:',
        },
        'mysql': {
            'host': '',
            'user': '',
            'password': '',
            'port': '',
        },
        'dict': {
        }
    }

    def __init__(self, **changed_keys):
        # TODO: описание настроек вынести в строку документации класса
        self.language = changed_keys.get('language', 'esperanto')
        self.history = changed_keys.get('history', False)
        self.monitor = changed_keys.get('monitor', True)  # включает вывод на экран статистику работы ИСУ
        self.logic = changed_keys.get('logic', True)  # включает модуль логики
        self.convert2IL = changed_keys.get('convert2IL', True)  # включает последний этап конвертации. Если при отключении включёна логика, то будет ошибка
        self.test = changed_keys.get('test', True)  # тестовый режим, включаемый в процессе отладки и разработки
        self.send_to_out = changed_keys.get('send_to_out')  # функция, в котору manspy пишет ответ. Устанавливается Интерфейсом
        self.ifname = changed_keys.get('ifname', '')  # уникальное имя интерфейса. Необходимо для журналов.

        # не рекомендуемые к изменению
        self.log_all = changed_keys.get('log_all', True)
        # 'real' - real answer, 'fake' - fake answer, 'construct' - construct answer
        self.answer_type = changed_keys.get('answer_type', 'fake')
        self.print_time = changed_keys.get('print_time', False)
        self.levels = changed_keys.get('levels', 'graphmath exec')

        paths_import = changed_keys.get('paths_import', [])
        self.paths_import.extend(paths_import)

    @classmethod
    def set_module(cls, module_type, module, module_code):
        cls.modules[module_type][module_code] = module

    @property
    def database(self):
        return self.modules['database'][self.db_type]

    def pass_args_to_logs(self, method_name, *args):
        if self.history:
            for logger_name, logger_class in self.modules['logger'].items():
                getattr(logger_class, method_name)(*args)


class InitSettings:
    """Класс, инициализирующий настройки"""
    _IS_ENTERED = False

    def __enter__(self):
        if self._IS_ENTERED:
            raise Exception('You should init `InitSettings` only one!')

        self._IS_ENTERED = True
        for module_type, path_import in Settings.paths_import:
            if module_type == 'action':
                fasif_parser(path_import, Settings(history=False))
            else:
                for module, module_code in importer.import_modules(path_import, module_type):
                    if module_type == 'logger':
                        module = module.Logger()
                    elif module_type == 'database':
                        config = Settings.db_settings[Settings.db_type]
                        module = module.Database(config)

                    Settings.set_module(module_type, module, module_code)

    def __exit__(self, Type, Value, Trace):
        for module_code, module in Settings.modules['logger'].items():
            module.close()

        for module_code, module in Settings.modules['database'].items():
            module.close()

        if Type is None:  # Если исключение не возникло
            pass
        else:             # Если возникло исключение
            return False  # False - исключение не обработано
                          # True  - исключение обработано
