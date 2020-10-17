class Settings:
    modules = {
        'language': {},
        'logger': {},
        'interface': {},
    }
    db_type = 'sqlite3'
    db_settings = {
        'sqlite3': {
            'path': 'database.db',
        },
        'mysql': {
            'host': '',
            'user': '',
            'password': '',
            'port': '',
        }
    }
    c = None
    cu = None

    def __init__(self, **changed_keys):
        # TODO: описание настроек вынести в строку документации класса
        self.language = changed_keys.get('language', 'esperanto')
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
        # 'real' - real answer, 'fake' - fake answer, 'construct' - construct answer
        self.answer_type = changed_keys.get('answer_type', 'fake')

    @classmethod
    def set_module(cls, module_type, module, module_code):
        cls.modules[module_type][module_code] = module
