import argparse
import pprint
import os.path
import os

from manspy.utils.settings import Settings, InitSettings
from manspy.utils.unit import Unit
from manspy.runners.simple import runner

console_cur_dir = os.path.abspath('')

READ = '\033[0;31m'
NORM = '\033[0;0m'
GREEN = '\033[0;32m'
ORANGE = '\033[0;33m'


def print_error(msg):
    print('{READ} {0} {NORM}'.format(msg, READ=READ, NORM=NORM))


class CLI:
    
    def __init__(self):
        self.settings = Settings(language='esperanto', answer_type='fake')

    def cmd_exec(self, args):
        def send_to_in(text, settings, level):
            results = runner(text, settings, pipeline=level)
            if isinstance(results, Unit):
                pprint.pprint(results.export_unit(ignore_units=dict))
            elif isinstance(results, dict):
                pprint.pprint(results)
            else:
                for result in results:
                    print(result)

        self.settings.language = args.language
        self.settings.answer_type = args.type
        self.settings.history = args.history
        # self.settings.print_time = args.print_time

        if args.text:
            send_to_in(args.text, self.settings, args.level)

        manspy_cur_dir = os.getcwd()
        for filename in args.filenames:
            os.chdir(console_cur_dir)
            filepath = os.path.abspath(filename)
            os.chdir(manspy_cur_dir)
            with open(filepath, 'r') as filef:
                send_to_in(filef.read(), self.settings)


def run(args_list=None):
    with InitSettings():
        cli = CLI()

        parser = argparse.ArgumentParser(description='ManSPy')
        parser.add_argument('--version', action='version', version='%(prog)s 0.0.0')

        parser.add_argument('--level', default='graphmath:exec')
        parser.add_argument('--type', default='fake', help='answer type: fake (default), construct, real')

        parser.add_argument('--language', default='esperanto', help='nature language')
        # parser.add_argument('--print-levels', action='store_true', help='print analysyses of every level')
        # parser.add_argument('--print-time', action='store_true', help='print time of every level')
        parser.add_argument('--history', action='store_true', help='save the history of dialog')
        parser.add_argument('--text', default=None, help='input text')
        parser.add_argument('filenames', nargs='*', help='files with input text')

        args = parser.parse_args(args_list)

        cli.cmd_exec(args)


if __name__ == '__main__':
    run()
