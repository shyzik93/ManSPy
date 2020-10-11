import json
import time
import os.path
import datetime
import uuid

from manspy.utils.beautifull_repr_data import (
    word_to_html,
    make_dialog_html_line,
    HTML_HEADER,
    INTERACTIVE_HTML_HEADER,
    INTERACTIVE_HTML_LINE_HEADER,
    INTERACTIVE_HTML_LINE_FOOTER
)

# TODO: добавить свойство `message_id`, состоящее из имени интерфейса, номера поотока и метки времени
class Message:
    """ Предоставляет для ManSPy функции для работы с вопросом/ответом и историей диалога  """

    def get_interface_id(self):
        return self.settings.ifname
        
    def get_message_id(self):
        return uuid.uuid1()

    def pass_args_to_all_logs(self, method_name, *args):
        if self.settings.history:
            for logger_name, logger_class in self.settings.modules['logger'].items():
                getattr(logger_class, method_name)(*args)

    def __init__(self, settings, text_settings, text=None, direction=None):
        self.settings = settings
        self.text_settings = text_settings
        self.r_texts = []

        #if not os.path.exists('history.html'):
        #    with open('history.html', 'w') as f:
        #        f.write(HTML_HEADER)
        #with open('history_interactive.html', 'w', encoding='utf-8') as f:
        #    f.write(INTERACTIVE_HTML_HEADER)

        self.pass_args_to_all_logs('on_create_message', direction, self)

        if direction == 'W': self.from_IF(text)
        elif direction == 'R': self.to_IF(text)

    def toString(self, r_text):
        if isinstance(r_text, (int, float, complex)): return str(r_text)
        else: return r_text

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

    # TODO: переименовать to_IF -> to_out (во вне)
    # TODO: переименовать r_text -> text_to_out (текст во вне)
    # TODO: переименовать self.settings['read_text'] -> self.settings['to_out']
    # TODO: переименовать "W" (Write) -> "Q" (Question), "R" (Read) -> "A" (Answer) 
    def to_IF(self, r_text):
        """ Вызывается функцией-глаголом (ManSPy) для передачи ответа в Интерфейс """
        r_text = self.toString(r_text)
        if r_text:
            self.pass_args_to_all_logs('log', 'R', r_text, self)
        self.settings.read_text(r_text, self.text_settings['any_data'])

    # TODO: переименовать from_IF -> from_out (из вне)
    # TODO: переименовать w_text -> text_from_out (текст из вне)
    # TODO: добавить опцию self.settings['from_out'] и в неё передавать вопрос
    def from_IF(self, w_text):
        """ Вызывается Интерфейсом для передачи вопроса в ManSPy """
        self.w_text = w_text
        if w_text:
            self.pass_args_to_all_logs('log', 'W', w_text, self)
        #self.save_interactive_html_line_header(w_text, "W", self.settings.ifname)

    def before_analyzes(self):
        """ Вызывается Модулем Анализа (ManSPy) """
        self.pass_args_to_all_logs('before_analyzes', self.text_settings['levels'], self)

    def before_analysis(self, level):
        """ Вызывается Модулем Анализа (ManSPy) """
        self.pass_args_to_all_logs('before_analysis', level, self)
        
    def after_analysis(self, level, sentences):
        """ Вызывается Модулем Анализа (ManSPy) """
        if self.settings.log_all:
            self.pass_args_to_all_logs('after_analysis', level, sentences, self)
        #if level == 'exec':
        #        self.save_interactive_html_line_footer()
