class Settings:
    modules = {
        'language': {},
        'logger': {},
        'interface': {},
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
        }
    }
    c = None
    cu = None

    def __init__(self, **changed_keys):
        # TODO: описание настроек вынести в строку документации класса
        self.language = changed_keys.get('language', 'esperanto')
        self.history = changed_keys.get('history', False)
        self.monitor = changed_keys.get('monitor', True)  # включает вывод на экран статистику работы ИСУ
        self.logic = changed_keys.get('logic', True)   # включает модуль логики
        self.convert2IL = changed_keys.get('convert2IL', True)  # включает последний этап конвертации
                               # если при отключении включёна логика, то будет ошибка
        self.test = changed_keys.get('test', True)  # тестовый режим, включаемый в процессе отладки и разработки
        self.send_to_out = changed_keys.get('send_to_out') # функция, в котору manspy пишет ответ. Устанавливается Интерфейсом
        self.ifname = changed_keys.get('ifname', '')  # уникальное имя интерфейса. Необходимо для журналов.
              # не рекомендуемые к изменению
        self.log_all = changed_keys.get('log_all', True)
        # 'real' - real answer, 'fake' - fake answer, 'construct' - construct answer
        self.answer_type = changed_keys.get('answer_type', 'fake')
        self.print_time = changed_keys.get('print_time', False)
        self.levels = changed_keys.get('levels', 'graphmath exec')

    @classmethod
    def set_module(cls, module_type, module, module_code):
        cls.modules[module_type][module_code] = module

    def pass_args_to_logs(self, method_name, *args):
        if self.history:
            for logger_name, logger_class in self.modules['logger'].items():
                getattr(logger_class, method_name)(*args)
