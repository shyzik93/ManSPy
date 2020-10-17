#! /usr/bin/env python3
import argparse
import pprint
import os.path

from manspy import API, Settings
from manspy.NLModules.ObjUnit import Unit

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
        def read_text(r_text, any_data):
            print(r_text)
        self.api = API()
        self.settings = Settings(read_text=read_text, language='esperanto', answer_type='fake')

    def __enter__(self):
        """ for 'with' statement """
        return self

    def __exit__(self, Type, Value, Trace):
        """ for 'with' statement """
        self.settings.c.close()

        if Type is None:  # Если исключение не возникло
            pass
        else:             # Если возникло исключение
            return False  # False - исключение не обработано
                          # True  - исключение обработано

    def cmd_exec(self, args):
        def write_text(text, settings, text_settings):
            msg, results = self.api.write_text(args.text, self.settings, text_settings)
            if isinstance(results, Unit):
                pprint.pprint(results.export_unit(ignore_units=dict))
            if isinstance(results, list):
                if results:
                    print('При выполнении возникли следующие ошибки:')
                for result in results:
                    print(result)

        self.settings.language = args.language
        self.settings.answer_type = args.type

        text_settings = {
            'levels': args.level,
            'print_time': args.print_time,
        }

        if args.text:
            write_text(args.text, self.settings, text_settings)

        manspy_cur_dir = os.getcwd()
        for filename in args.filenames:
            os.chdir(console_cur_dir)
            filepath = os.path.abspath(filename)
            os.chdir(manspy_cur_dir)
            with open(filepath, 'r') as filef:
                write_text(filef.read(), self.settings, text_settings)


def do_cmd(args_list=None):

    # TODO: добавить опцию `manspy --run-interface *` для параллельного запуска перечисленных интерфейсов. Соответственно, файл manspy/run.py следует удалить.

    with CLI() as cli:

        parser = argparse.ArgumentParser(description='ManSPy')
        parser.add_argument('--version', action='version', version='%(prog)s 0.0.0')

        parser.add_argument('--level', default='graphmath exec')
        parser.add_argument('--type', default='fake', help='answer type')

        parser.add_argument('--language', default='esperanto', help='nature language')
        # arser.add_argument('--print-levels', action='store_true', help='print analysyses of every level')
        parser.add_argument('--print-time', action='store_true', help='print time of every level')
        parser.add_argument('--text', default=None, help='input text')
        parser.add_argument('filenames', nargs='*', help='files with input text')

        args = parser.parse_args(args_list)

        cli.cmd_exec(args)
