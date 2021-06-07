#! /usr/bin/env python3
import argparse
import pprint
import os.path

from manspy.analyse_text import nature2internal
from manspy.message import Message
from manspy.utils.settings import Settings
from manspy.unit import Unit

console_cur_dir = os.path.abspath('')

READ = '\033[0;31m'
NORM = '\033[0;0m'
GREEN = '\033[0;32m'
ORANGE = '\033[0;33m'


def print_error(msg):
    print('{READ} {0} {NORM}'.format(msg, READ=READ, NORM=NORM))


def proc_answer(is_success, arg1):
    if not is_success:
        print_error(arg1)
        exit(2)


class CLI:
    
    def __init__(self):
        self.settings = Settings(language='esperanto', answer_type='fake')

    '''def __enter__(self):
        """ for 'with' statement """
        return self

    def __exit__(self, Type, Value, Trace):
        """ for 'with' statement """
        self.settings.c.close()

        if Type is None:  # Если исключение не возникло
            pass
        else:             # Если возникло исключение
            return False  # False - исключение не обработано
                          # True  - исключение обработано'''

    def cmd_exec(self, args):
        def send_to_in(text, settings):
            results = nature2internal(Message(settings, text))
            if isinstance(results, Unit):
                pprint.pprint(results.export_unit(ignore_units=dict))
            elif isinstance(results, (dict, list)):
                pprint.pprint(results)
            else:
                for result in results:
                    print(result)

        self.settings.language = args.language
        self.settings.answer_type = args.type
        self.settings.history = args.history
        self.settings.print_time = args.print_time
        self.settings.levels = args.level

        if args.text:
            send_to_in(args.text, self.settings)

        manspy_cur_dir = os.getcwd()
        for filename in args.filenames:
            os.chdir(console_cur_dir)
            filepath = os.path.abspath(filename)
            os.chdir(manspy_cur_dir)
            with open(filepath, 'r') as filef:
                send_to_in(filef.read(), self.settings)


def do_cmd(args_list=None):

    # TODO: добавить опцию `manspy --run-interface *` для параллельного запуска перечисленных интерфейсов. Соответственно, файл manspy/run.py следует удалить.

    with Settings():
        cli = CLI()

        parser = argparse.ArgumentParser(description='ManSPy')
        parser.add_argument('--version', action='version', version='%(prog)s 0.0.0')

        parser.add_argument('--level', default='graphmath:exec')
        parser.add_argument('--type', default='fake', help='answer type: fake (default), construct, real')

        parser.add_argument('--language', default='esperanto', help='nature language')
        # parser.add_argument('--print-levels', action='store_true', help='print analysyses of every level')
        parser.add_argument('--print-time', action='store_true', help='print time of every level')
        parser.add_argument('--history', action='store_true', help='save the history of dialog')
        parser.add_argument('--text', default=None, help='input text')
        parser.add_argument('filenames', nargs='*', help='files with input text')

        args = parser.parse_args(args_list)

        cli.cmd_exec(args)
