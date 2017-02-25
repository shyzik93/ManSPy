# -*- coding: utf-8 -*-

import time, json

class Message:

    ''' Создан пока только для: логирования с учётом уникального номера сообщения; передачи настроек текущего потока '''

    def __init__(self, message_nl, direction, settings):
        self.settings = settings
        self.direction = direction
        self.nl = message_nl # nl = Nature Language
        self.il = None # il = Internal Language

        self.c, self.cu = self.settings['db_sqlite3']

        self.cu.execute('''
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
	    ''')

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

    def log(self, row_name, row_value):
    	if isinstance(row_value, (dict, list)): row_value = json.dumps(row_value)
    	self.cu.execute('UPDATE `log_history` SET `'+row_name+'`=? WHERE `message_id`=?', (row_value, self.message_id));
    	self.c.commit()