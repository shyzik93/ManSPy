import json
import time
import os.path
import datetime

from manspy.utils.beautifull_repr_data import (
    word_to_html,
    make_dialog_html_line,
    make_dialog_plain_line,
    HTML_HEADER,
    INTERACTIVE_HTML_HEADER,
    INTERACTIVE_HTML_LINE_HEADER,
    INTERACTIVE_HTML_LINE_FOOTER
)

# TODO: добавить свойство `message_id`, состоящее из имени интерфейса, номера поотока и метки времени
class Message:
    """ Предоставляет для ManSPy функции для работы с вопросом/ответом и историей диалога  """

    def __init__(self, settings, text_settings, text=None, direction=None):
        self.settings = settings
        self.text_settings = text_settings
        self.r_texts = []

        if not os.path.exists('history.html'):
            with open('history.html', 'w') as f:
                f.write(HTML_HEADER)
        with open('history_interactive.html', 'w') as f:
            f.write(INTERACTIVE_HTML_HEADER)

        if direction == 'W': self.from_IF(text)
        elif direction == 'R': self.to_IF(text)

        '''self.settings = settings
        self.direction = direction
        self.nl = message_nl # nl = Nature Language
        self.il = None # il = Internal Language

        self.c, self.cu = self.settings.db_sqlite3

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
          (self.direction, self.settings.thread_name, self.settings.language, self.nl)
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

    def save_plain_line(self, text, direction, ifname):
        if self.settings.history and text:
            with open('history.txt', 'ab') as f:
                f.write(bytearray(make_dialog_plain_line(text, direction, ifname), 'utf-8'))

    def save_html_line(self, text, direction, ifname):
        """ Сейчас выходной текст явлется строкой, но когда он станет классом,
            то мы уберём данное условие (подусловный блок останется)"""
        if direction == "W":
            text_ = []
            for index, cSentence in text:
                for index, cWord in cSentence.subunits_copy.items():
                    text_.append(word_to_html(cWord))
            text = ' '.join(text_)

        with open('history.html', 'a') as f:
            f.write(make_dialog_html_line(text, direction))

    def save_interactive_html_line_header(self, text, direction, ifname):
        with open('history_interactive.html', 'a') as f:
            f.write(INTERACTIVE_HTML_LINE_HEADER.format(
                message_id='MESSAGE_ID',  # TODO: MESSAGE_ID
                space='',
                direction=direction,
                thread_name='THREAD_NAME',#self.settings['thread_name'],
                language=self.settings.language,
                date_add='DATE_ADD',  # TODO: DATE_ADD
                text=text
            ))

    def save_interactive_html_line_footer(self):
        with open('history_interactive.html', 'a') as f:
            f.write(INTERACTIVE_HTML_LINE_FOOTER)


    # TODO: переименовать to_IF -> to_out (во вне)
    # TODO: переименовать r_text -> text_to_out (текст во вне)
    # TODO: переименовать self.settings['read_text'] -> self.settings['to_out']
    # TODO: переименовать "W" (Write) -> "Q" (Question), "R" (Read) -> "A" (Answer) 
    def to_IF(self, r_text):
        """ Вызывается функцией-глаголом (ManSPy) для передачи ответа в Интерфейс """
        r_text = self.toString(r_text)
        self.save_plain_line(r_text, "R", self.settings.ifname)
        self.save_html_line(r_text, 'R', self.settings.ifname)
        self.settings.read_text(r_text, self.text_settings['any_data'])

    # TODO: переименовать from_IF -> from_out (из вне)
    # TODO: переименовать w_text -> text_from_out (текст из вне)
    # TODO: добавить опцию self.settings['from_out'] и в неё передавать вопрос
    def from_IF(self, w_text):
        """ Вызывается Интерфейсом для передачи вопроса в ManSPy """
        self.w_text = w_text
        self.save_plain_line(w_text, "W", self.settings.ifname)
        self.save_interactive_html_line_header(w_text, "W", self.settings.ifname)

    def before_analysises(self):
        """ Вызывается Модулем Анализа (ManSPy) """
        with open('analysis.txt', 'a', encoding='utf-8') as f:
            f.write('\n\n'+'#'*100+'\n')
            f.write(self.text_settings['levels']+'\n')

    def before_analysis(self, level):
        """ Вызывается Модулем Анализа (ManSPy) """
        now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        with open('analysis.txt', 'a', encoding='utf-8') as f:
            f.write('----'+now+'\n')
            #f.fwrite('Folding sentence: '+str(sentence.getUnit('str'))+'\n')
            f.write(('- '*10)+level+(' -'*10)+u'\n')
        
    def after_analysis(self, level, sentences):
        """ Вызывается Модулем Анализа (ManSPy) """
        if level == 'synt':
            self.save_html_line(sentences, 'W', self.settings.ifname)

        if self.settings.log_all:
            if level == "graphmath":
                with open('analysis.txt', 'a', encoding='utf-8') as f:
                    f.write('NL-sentence: ')
                    for index, sentence in sentences:
                        for index, word in sentence.subunits_copy.items(): f.write(word['word']+' ')
                    f.write('\n')
                sentences = sentences.getUnit('dict')
            elif level == 'morph':
                pass
                with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
                    flog.write('\n')
                    for index, sentence in sentences: flog.write('sentence: %s\n' % sentence.getUnit('str')['fwords'])
                    flog.write('\n')
    
                sentences = sentences.getUnit('dict')            
            elif level == 'postmorph':
                sentences = sentences.getUnit('dict')
            elif level == 'synt':
                sentences = sentences.getUnit('dict')
            elif level == 'extract':
                sentences = list(sentences)
                return
            elif level == 'convert':
                _res = []
                for index, ILs in sentences.items():
                    for IL in ILs:
                        _res.append('IL-sentence: '+str(IL))
                sentences = _res
    
            with open('analysis.txt', 'a', encoding='utf-8') as f: 
                json.dump(sentences, f, sort_keys=True, indent=4)#.replace('"', '')
                f.write('\n')
            
            
            if level == 'exec':
                self.save_interactive_html_line_footer()

    #def log(self, row_name, row_value):
    #    #if isinstance(row_value, (dict, list)): row_value = json.dumps(row_value)
    #    #self.cu.execute('UPDATE `log_history` SET `'+row_name+'`=? WHERE `message_id`=?', (row_value, self.message_id));
    #    #self.c.commit()
    #    pass