from dataclasses import dataclass
import uuid


# TODO: добавить свойство `message_id`, состоящее из имени интерфейса, номера поотока и метки времени
class Message:
    """ Предоставляет для ManSPy функции для работы с вопросом/ответом и историей диалога  """

    def get_interface_id(self):
        return self.settings.ifname

    @property
    def id(self):
        if not self._message_id:
            self._message_id = uuid.uuid1().hex

        return self._message_id

    def __init__(self, settings, text=None, any_data=None, direction='W'):
        self.settings = settings
        self.any_data = any_data
        self.text = text
        self._message_id = None
        self.analysis = {}
        self.pass_args_to_logs('on_create_message', direction, text, self)

        if direction == 'W':
            if text:
                self.pass_args_to_logs('log', 'W', text, self)
        elif direction == 'R':
            self.send_to_out(text)

    def pass_args_to_logs(self, method_name, *args):
        if self.settings.history:
            for logger_class in self.settings.loggers:
                getattr(logger_class, method_name)(*args)

    def toString(self, r_text):
        if isinstance(r_text, (int, float, complex)):
            return str(r_text)
        else:
            return r_text

    # TODO: переименовать "W" (Write) -> "Q" (Question), "R" (Read) -> "A" (Answer) 
    def send_to_out(self, text_to_out):
        """ Вызывается функцией-глаголом (ManSPy) для передачи ответа в Интерфейс """
        text_to_out = self.toString(text_to_out)
        if text_to_out:
            self.settings.pass_args_to_logs('log', 'R', text_to_out, self)
            self.settings.send_to_out(text_to_out, self.any_data)

    def before_analyzes(self, levels):
        """ Вызывается Модулем Анализа (ManSPy) """
        self.pass_args_to_logs('before_analyzes', levels, self)

    def before_analysis(self, level):
        """ Вызывается Модулем Анализа (ManSPy) """
        self.pass_args_to_logs('before_analysis', level, self)
        
    def after_analysis(self, level, sentences):
        """ Вызывается Модулем Анализа (ManSPy) """
        self.pass_args_to_logs('after_analysis', level, sentences, self)

    def after_analyzes(self, levels):
        self.pass_args_to_logs('after_analyzes', levels, self)
