import time

from . import history
from manspy.utils.beautiful_repr_data import (
    make_dialog_plain_line
)

class Message:

    ''' Создан пока только для: логирования с учётом уникального номера сообщения; передачи настроек текущего потока '''

    def __init__(self, settings, text_settings, text=None, direction=None):
        self.settings = settings
        self.text_settings = text_settings
        self.r_texts = []

        # TODO: Объект истории передавать в аргументе __init__
        self.history = history.History()

        if direction == 'W': self.from_IF(text)
        elif direction == 'R': self.to_IF(text)

        '''self.settings = settings
        self.direction = direction
        self.nl = message_nl # nl = Nature Language
        self.il = None # il = Internal Language

        self.c, self.cu = self.settings['db_sqlite3']

        self.cu.execute(\'''
        CREATE TABLE IF NOT EXISTS `log_history` (
          `message_id` INTEGER PRIMARY KEY AUTOINCREMENT,
          `direction` TEXT,
          `thread_name` VARCHAR(255),
          `language` INTEGER,
          `date_add` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `message_nl` TEXT,
          `message_il` JSON,
          `a_graphemath` JSON,
          `a_morph` JSON,
          `a_postmorph` JSON,
          `a_synt` JSON);
      \''')

        t1 = time.time()
        self.cu.execute(
          'INSERT INTO `log_history` (`direction`, `thread_name`, `language`, `message_nl`) VALUES (?, ?, ?, ?);',
          (self.direction, self.settings['thread_name'], self.settings['language'], self.nl)
        )
        t2 = time.time()
        _t1 = t2 - t1
        self.c.commit()
        t3 = time.time()
        _t2 = t3 - t2
        #print(_t1, _t2)


        self.message_id = self.cu.lastrowid
        #print(self.message_id)"""
        '''

    def toString(self, r_text):
        if isinstance(r_text, (int, float, complex)): return str(r_text)
        else: return r_text

    def save_plain_line(text, direction, ifname):
        if self.settings['history'] and text
            with open('history.txt', 'ab') as f:
                f.write(bytearray(make_dialog_plain_line(text, direction, ifname), 'utf-8'))

    # TODO: переименовать to_IF -> to_out (во вне)
    # TODO: переименовать r_text -> text_to_out (текст во вне)
    def to_IF(self, r_text):
        r_text = self.toString(r_text)
        self.save_plain_line(r_text, "R", self.settings['ifname'])
        self.history.html(r_text, 'R')
        self.settings['read_text'](r_text, self.text_settings['any_data'])

    # TODO: переименовать from_IF -> from_out (из вне)
    # TODO: переименовать w_text -> text_from_out (текст из вне)
    def from_IF(self, w_text):
        self.w_text = w_text
        self.save_plain_line(w_text, "W", self.settings['ifname'])

    #def log(self, row_name, row_value):
    #    #if isinstance(row_value, (dict, list)): row_value = json.dumps(row_value)
    #    #self.cu.execute('UPDATE `log_history` SET `'+row_name+'`=? WHERE `message_id`=?', (row_value, self.message_id));
    #    #self.c.commit()
    #    pass