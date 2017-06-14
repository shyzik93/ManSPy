#! /usr/bin/env python3

import argparse
import os
import pprint

import manspy

READ = '\033[0;31m'
NORM = '\033[0;0m'
GREEN= '\033[0;32m'
ORANGE = '\033[0;33m'

def print_error(msg):
    print('{READ} {0} {NORM}'.format(msg, READ=READ, NORM=NORM))

def proc_answer(is_success, arg1):
    if not is_success:
        print_error(arg1)
        exit(2)

'''
    CLI.cmd_run:
        @todo при ошибке в аргшументах эта ошибка должна только отобразиться на экране, но программа не должна завершаться.
        @todo аргументы должны парситься стандартным образом, а не с помощью split()
    API.update_settings_for_IF:
        @todo переименовать эту функцию в update_settings

    Класс настроек, реализующий трёхуровневый стек настроек:
    - настройки интерфейса по умолчанию
    - настройки интерфейса
    - настройки интерфейса для конкретного сообщения.
'''

class CLI():
    
    def __init__(self):
        self.api = manspy.API()
        self.settings = {'read_text': self.read_text}
        self.api.update_settings_for_IF(self.settings)

    def __enter__(self):
        ''' for 'with' statement '''
        return self

    def __exit__(self, Type, Value, Trace):
        ''' for 'with' statement '''
        c, cu = self.settings['db_sqlite3']
        c.close()

        if Type is None:  # Если исключение не возникло
            pass
        else:             # Если возникло исключение
            return False  # False - исключение не обработано
                          # True  - исключение обработано

    def read_text(self, r_text, any_data):
        print(r_text)

    def cmd_exec(self, args):
        levels = ':exec' # усли не указан ни один анализ
        for index, level in enumerate([args.graph, args.morph, args.pmorph, args.synt, args.extract, args.convert]): # exec не указываем, так как он поумолчанию
            if level:
                levels = ':' + self.api.LangClass.levels[index]
                break

        self.settings['language'] = args.language
        msg, res = self.api.write_text(args.msg, self.settings, {'levels': levels, 'print_time':False})

        if args.graph or args.morph or args.pmorph or args.synt:
            e = res.export_unit()
            print()
            print('Properties of text:')
            del e['unit_info']['max_index']
            pprint.pprint(e['unit_info'])

            for index, sentence in e['unit'].items():
                print()
                print('Properties of sentence:')
                del sentence['unit_info']['max_index']
                pprint.pprint(sentence['unit_info'])

                for index, word in sentence['unit'].items():
                    print()
                    print('Properties of word:')
                    del word['unit_info']['max_index'], word['unit_info']['type'], word['unit_info']['notword'], word['unit_info']['end_orig'], word['unit_info']['end_pmark'], word['unit_info']['start_pmark']
                    pprint.pprint(word['unit_info'])
            #pprint.pprint(res)

        #print(res)

    def cmd_run(self, args):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')

        subparser = subparsers.add_parser('if', help='run or stop interfaces. For example: +if_name1 +if_name2 -if_name3 -if_name4')
        subparser.add_argument('interfaces', nargs='+')

        subparser = subparsers.add_parser('exec', help='execute nature language')

        subparser = subparsers.add_parser('lang', help='change language for interface')
        subparser.add_argument('interface')
        subparser.add_argument('language')

        subparser = subparsers.add_parser('exit', help='exit from ManSPy')

        while 1:
            str_args = input('Insert command:\n')
            try:
                args = parser.parse_args(str_args.split())
            except:
                continue
            if args.command == 'exit': break



def do_cmd():

    with CLI() as cli:

        parser = argparse.ArgumentParser(description='Management system')
        subparsers = parser.add_subparsers(dest='command')
        parser.add_argument('--version', action='version', version='%(prog)s 0.0.0')

        subparser = subparsers.add_parser('exec', help='execute nature language')
        subparser.add_argument('-i', '--image', action='store_false', help='use unreal data source for answers. For example, if your Internet is slow, or you don\'t have one.')
        subparser.add_argument('--graph', action='store_true')
        subparser.add_argument('--morph', action='store_true')
        subparser.add_argument('--pmorph', action='store_true')
        subparser.add_argument('--synt', action='store_true')
        subparser.add_argument('--extract', action='store_true')
        subparser.add_argument('--convert', action='store_true') # до какого уровня делать включительно
        subparser.add_argument('-l', '--language', default='Esperanto', help='Nature language')
        subparser.add_argument('-v', '--verbose', action='store_false', help='Print analysyses')
        subparser.add_argument('msg')

        subparser = subparsers.add_parser('run', help='run the manspy\'s interfaces')
        subparser.add_argument('-i', '--image', action='store_false', help='use unreal data source for answers. For example, if your Internet is slow, or you don\'t have one.')
        
        args = parser.parse_args()
         
        if args.command is not None:
            func = getattr(cli, 'cmd_'+args.command)
            res = func(args)