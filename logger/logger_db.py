import json

from manspy.unit import Word, Sentence, Text


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Text, Sentence, Word)):
            return obj.export_unit()
        else:
            return str(obj)


class LoggerDb:
    def connect_to_db(self, settings):
        self.c, self.cu = settings.c, settings.cu

        # self.cu.execute('''
        # CREATE TABLE IF NOT EXISTS `log_history` (
        #   `message_id` INTEGER PRIMARY KEY AUTOINCREMENT,
        #   `direction` VARCHAR(1),
        #   `thread_name` VARCHAR(255),
        #   `language` INTEGER,
        #   `date_add` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        #   `message_nl` TEXT,
        #   `message_il` JSON,
        #   `a_graphmath` JSON,
        #   `a_morph` JSON,
        #   `a_postmorph` JSON,
        #   `a_synt` JSON,
        #   `a_extract` JSON,
        #   `a_convert` JSON,
        #   `a_exec` JSON);''')
        # self.c.commit()

    def __init__(self):
        self.c = None
        self.cu = None

    def on_create_message(self, direction, msg):
        if self.c is None:
            self.connect_to_db(msg.settings)
        msg.logger_db_message_id = None

    def log(self, direction, text, msg):
        if self.c is None:
            self.connect_to_db(msg.settings)
        self.cu.execute(
          'INSERT INTO `log_history` (`direction`, `thread_name`, `language`, `message_nl`) VALUES (?, ?, ?, ?);',
          (direction, 'msg.settings.thread_name', msg.settings.language, text)
        )
        self.c.commit()

        if msg.logger_db_message_id is None:
            msg.logger_db_message_id = self.cu.lastrowid

    def before_analyzes(self, levels, msg):
        pass

    def before_analysis(self, level, msg):
        pass

    def after_analysis(self, level, sentences, msg):
        sentences = json.dumps(sentences, cls=ComplexEncoder)
        self.cu.execute(
            'UPDATE `log_history` SET `a_{}`=? WHERE `message_id`=?'.format(level),
            (sentences, msg.logger_db_message_id)
        )
        self.c.commit()

    def close(self):
        pass
