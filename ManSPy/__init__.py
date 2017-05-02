""" Предоставляет API интеллекта, который используется модулями интерфейса.
    В качестве API:
      API = ISM.API(Settings) # Settings - словарь, задающий настройки.
    Примеры возможных интерфейсов: текстовый чат, распознаватель речи,
    мессенджеры, интерфейс мозг-компьютер, приёмник звонков и SMS и так далее.
"""
import time, sys, os, copy, json, datetime
from . import FCModule, import_action
from .analyse_text import LangClass

import sqlite3 as sql

sql.enable_callback_tracebacks(True)

def create_bd_file(language, name):
    if not os.path.exists(language) or not os.path.isdir(language):
        os.mkdir(language) # хдесь бывает ошибка, так, видимо, эта функция вызывается параллельно где-то в другом потоке
    name = os.path.join(language, name)
    c = sql.connect(name)
    c.row_factory = sql.Row
    cu = c.cursor()
    return c, cu

class MainException(Exception): pass


class History:
    def __init__(self):
         if not os.path.exists('history.html'): self.html_head()

    def plain(self, sText, direction, IF):
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()-time.altzone))
        if direction == 'R': sText = '   '+sText
        sText = "* %s  %s  %s: %s\n" % (direction, Time, IF.IFName, sText)
        with open('history.txt', 'ab') as f: f.write(bytearray(sText, 'utf-8'))

    def html_head(self):
        with open('history.html', 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="ru"><head>
    <meta charset="utf-8">
</head><body>
    <style>
        .supplement {
            color: #007df8;
         }
         .subject {
         }
         .direct_supplement {
             color: blue;
         }
         .predicate {
             color: green;
         }
         .circumstance {
             color: yellow
         }
         .definition {
             color: #bf8419
         }
    </style>
""")

    def html_row(self, sText, direction):
        with open('history.html', 'a') as f:
            f.write("""    {0} &nbsp;&nbsp; {1}<br>""".format(direction, sText))

    def html_build_word(self, cWord):
        return """<span class="word{MOSentence}">{word}</span>""".format(
            word=cWord['word'],
            MOSentence=' '+cWord['MOSentence'].replace(' ', '_') if 'MOSentence' in cWord else ''
        )

    def html_build_text(self, cText):
        text_ = []

        for index, cSentence in cText:
            for index, cWord in cSentence.subunits_copy.items():
                text_.append(self.html_build_word(cWord))

        return ' '.join(text_)

    def html(self, mText, direction):
        if direction == "W": self.html_row(self.html_build_text(mText), direction)
        else: self.html_row("&nbsp;"*8 + mText, direction)


    def log(self, title, res):

        if title == "graphmath":
            with open('analysis.txt', 'a', encoding='utf-8') as f:
                f.write('NL-sentence: ')
                for index, sentence in res:
                    for index, word in sentence.subunits_copy.items(): f.write(word['word']+' ')
                f.write('\n')
            res = res.getUnit('dict')
        elif title == 'morph':
            pass
            with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
                flog.write('\n')
                for index, sentence in res: flog.write('sentence: %s\n' % sentence.getUnit('str')['fwords'])
                flog.write('\n')

            res = res.getUnit('dict')            
        elif title == 'postmorph':
            res = res.getUnit('dict')
        elif title == 'synt':
            self.html(res, 'W')
            res = res.getUnit('dict')
        elif title == 'extract':
            res = list(res)
            return
        elif title == 'convert':
            _res = []
            for index, ILs in res.items():
                for IL in ILs:
                    _res.append('IL-sentence: '+str(IL))
            res = _res

        now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        with open('analysis.txt', 'a', encoding='utf-8') as f:
            f.write('----'+now+'\n')
            #f.fwrite('Folding sentence: '+str(sentence.getUnit('str'))+'\n')
            f.write(('- '*10)+title+(' -'*10)+u'\n')

            json.dump(res, f, sort_keys=True, indent=4)#.replace('"', '')
            f.write('\n')

class Message:

    ''' Создан пока только для: логирования с учётом уникального номера сообщения; передачи настроек текущего потока '''

    def __init__(self, IF, direction=None, text=None, any_data=None):
        self.IF = IF
        self.r_texts = []

        self.history = History()

        if direction == 'W': self.from_IF(text)
        elif direction == 'R': self.to_IF(text)

        self.any_data = any_data

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

    '''def _save_history(self, text, Type):
        if text:
            Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()-time.altzone))
            if Type == 'R': text = '   '+text
            text = "* %s  %s  %s: %s\n" % (Type, Time, self.IF.IFName, text)
            with open('history.txt', 'ab') as f: f.write(bytearray(text, 'utf-8'))'''

    def toString(self, r_text):
        if isinstance(r_text, (int, float, complex)): return str(r_text)
        else: return r_text

    def to_IF(self, r_text):
        r_text = self.toString(r_text)
        #if self.IF.settings['history']: self._save_history(r_text, "R")
        if self.IF.settings['history'] and r_text: self.history.plain(r_text, "R", self.IF)
        self.history.html(r_text, 'R')
        self.IF.read_text(r_text, self.any_data)

    def from_IF(self, w_text):
        self.w_text = w_text
        #if self.IF.settings['history']: self._save_history(w_text, "W")
        if self.IF.settings['history'] and w_text: self.history.plain(w_text, "W", self.IF)



    #def log(self, row_name, row_value):
    #    #if isinstance(row_value, (dict, list)): row_value = json.dumps(row_value)
    #    #self.cu.execute('UPDATE `log_history` SET `'+row_name+'`=? WHERE `message_id`=?', (row_value, self.message_id));
    #    #self.c.commit()
    #    pass


class API():
    # настройки задаются один раз. Но можно написать модуль для изменения
    # настроек через канал общения.
    default_settings = {'history': True,
              'monitor': True, # включает вывод на экран статистику работы ИСУ
              'logic': True, # включает модуль логики
              'convert2IL': True, # включает последний этап конвертации
                               # если при отключении включёна логика, то будет ошибка
              'language': 'Esperanto',
              'test': True, # тестовый режим, включаемый в процессе отладки и разработки

              # не рекомендуемые к изменению
              'log_all': False,
              'storage_version': 2,
              'assoc_version': 3,
              'dir_db': None,
              'db_sqlite3': None,
    }

    def make_db_dir(self, db_path=None):
        # Устанавливаем путь к директории базы данных как рабочую (текущую)
        if db_path is None: db_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(db_path, 'DATA_BASE')
        if not os.path.exists(db_path) or not os.path.isdir(db_path):
            os.mkdir(db_path)
        os.chdir(db_path)
        return db_path

    def update_settings_for_IF(self, settings):
        # Проверяем правильность ключей
        keys = self.default_settings.keys()
        for user_key in settings.keys():
            if user_key not in keys:
                raise MainException('error2: Wrong name of key in settings: %s' % str(user_key))
        # Обновляем настройки
        _settings = copy.deepcopy(self.default_settings) # Создаём новые настройки. Только при инициализации даннгого класса в модуле run.py
        _settings.update(settings)
        settings.update(_settings)
        # Корректируем настройки
        settings['language'] = settings['language'].capitalize()
        settings['db_sqlite3'] = create_bd_file(settings['language'], 'main_data.db')

    def __init__(self):
        self.default_settings['dir_db'] = self.make_db_dir(self.default_settings['dir_db'])

        """ Инициализация ManSPy """
        #settings = copy.deepcopy(self.default_settings)
        #self.update_settings_for_IF(settings)
        # Меняем настройки по умолчанию на пользовательские

        print("Init nature language's module...")
        t1 = time.time()
        self.LangClass = LangClass()
        t2 = time.time()
        print('  ', t2 - t1)

        print("Init action's modules...")
        t1 = time.time()
        self.action_importer = import_action.ImportAction(self.LangClass, self.default_settings['assoc_version'])
        #self.action_importer.fsf2json()
        self.was_imported = {}
        t2 = time.time()
        print('  ', t2 - t1)

        print("Init functions's module...")
        t1 = time.time()
        self.LogicShell = FCModule.LogicShell()
        t2 = time.time()
        print('  ', t2 - t1)
        print("Ready!")

    def write_text(self, IF, w_text, any_data=None):
        '''
            any_data - any data, if you would like to pass it to IF with answer.
        '''
        #print(threading.current_thread().name)

        if IF.settings['language'] not in self.was_imported:

            print("Import fasifs for {0} language...".format(IF.settings['language']))
            t1 = time.time()

            self.action_importer.import_for_lang(IF.settings)
            self.was_imported[IF.settings['language']] = True

            t2 = time.time()
            print('  ', t2 - t1)

        w_msg = Message(IF, 'W', w_text, any_data)
        if w_text:
            t =time.time()
            w_msg.ils = self.LangClass.NL2IL(w_msg)
            w_msg.time_total = time.time()-t
            print('       Total: ', w_msg.time_total)
            ExecError = self.LogicShell.execIL(w_msg)
            return w_msg