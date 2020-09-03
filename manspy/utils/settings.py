class Settings:
    modules = {
        'language': {},
        'logger': [],
    }
    db = None
    db_sqlite3 = None
    dir_db = None
    storage_version = 2
    assoc_version = 3

    def __init__(self, **changed_keys):
        self.language = changed_keys.get('language', 'Esperanto')
        self.history = changed_keys.get('history', True)
        self.monitor = changed_keys.get('monitor', True)  # включает вывод на экран статистику работы ИСУ
        self.logic = changed_keys.get('logic', True)   # включает модуль логики
        self.convert2IL = changed_keys.get('convert2IL', True)  # включает последний этап конвертации
                               # если при отключении включёна логика, то будет ошибка
        self.test = changed_keys.get('test', True)  # тестовый режим, включаемый в процессе отладки и разработки
        self.read_text = changed_keys.get('read_text') # функция, в котору manspy пишет ответ. Устанавливается Интерфейсом
        self.ifname = changed_keys.get('ifname', '')  # уникальное имя интерфейса. Необходимо для журналов.
              # не рекомендуемые к изменению
        self.log_all = changed_keys.get('log_all', True)

    @classmethod
    def set_module(cls, module_type, module, module_code=None):
        if isinstance(cls.modules[module_type], list):
            cls.modules[module_type].append(module)
        elif isinstance(cls.modules[module_type], dict):
            cls.modules[module_type][module_code] = module
    