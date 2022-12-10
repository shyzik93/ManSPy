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

        # if not os.path.exists('history.html'):
        #    with open('history.html', 'w') as f:
        #        f.write(HTML_HEADER)
        # with open('history_interactive.html', 'w', encoding='utf-8') as f:
        #    f.write(INTERACTIVE_HTML_HEADER)
        self.settings.pass_args_to_logs('on_create_message', direction, text, self)

        if direction == 'W':
            if text:
                self.settings.pass_args_to_logs('log', 'W', text, self)
                # self.save_interactive_html_line_header(w_text, "W", self.settings.ifname)
        elif direction == 'R':
            self.send_to_out(text)

    def toString(self, r_text):
        if isinstance(r_text, (int, float, complex)):
            return str(r_text)
        else:
            return r_text

    '''def save_interactive_html_line_header(self, text, direction, ifname):
        with open('history_interactive.html', 'a', encoding='utf-8') as f:
            f.write(INTERACTIVE_HTML_LINE_HEADER.format(
                message_id='MESSAGE_ID',  # TODO: MESSAGE_ID
                space='',
                direction=direction,
                thread_name='THREAD_NAME',#self.settings['thread_name'],
                language=self.settings.language,
                date_add='DATE_ADD',  # TODO: DATE_ADD
                text=text
            ))'''

    '''def save_interactive_html_line_footer(self):
        with open('history_interactive.html', 'a', encoding='utf-8') as f:
            f.write(INTERACTIVE_HTML_LINE_FOOTER)'''

    # TODO: переименовать "W" (Write) -> "Q" (Question), "R" (Read) -> "A" (Answer) 
    def send_to_out(self, text_to_out):
        """ Вызывается функцией-глаголом (ManSPy) для передачи ответа в Интерфейс """
        text_to_out = self.toString(text_to_out)
        if text_to_out:
            self.settings.pass_args_to_logs('log', 'R', text_to_out, self)
            self.settings.send_to_out(text_to_out, self.any_data)

    def before_analyzes(self):
        """ Вызывается Модулем Анализа (ManSPy) """
        pass# self.settings.pass_args_to_logs('before_analyzes', self.settings.levels, self)

    def before_analysis(self, level):
        """ Вызывается Модулем Анализа (ManSPy) """
        self.settings.pass_args_to_logs('before_analysis', level, self)
        
    def after_analysis(self, level, sentences):
        """ Вызывается Модулем Анализа (ManSPy) """
        if self.settings.log_all:
            self.settings.pass_args_to_logs('after_analysis', level, sentences, self)
        # if level == 'exec':
        #        self.save_interactive_html_line_footer()
