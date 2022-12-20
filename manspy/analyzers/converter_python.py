import itertools

from manspy.analyzers import utils
from manspy.storage.fasif.finder import find
from manspy.storage.relation import Relation
from manspy.utils.unit import Sentence
from manspy.utils import importer


import ast
import astor


def build_main_tree(body):
    function_execute = ast.FunctionDef(body=body, name='execute', decorator_list=[], args=ast.arguments(args=[], defaults=[], vararg=None, kwarg=None))
    module_body = []
    module_body.append(function_execute)
    return ast.Module(body=module_body)


def Extraction2IL(relation, settings, subjects, predicate, arguments):
    body = []

    args = [ast.Name(id='arg0')]
    keywords = [ast.keyword(arg='arg01', value=ast.Name(id='arg1'))]
    body.extend([
        ast.ImportFrom(module='manspy.action.currency', level=0, names=[ast.alias(name='GetCourse', asname=None)]),
        ast.Assign(
            targets=[ast.Name(id='arg0')],
            value=ast.Dict(keys=[ast.Name(id='answer_type')], values=[ast.Str(settings.answer_type)]),
        ),
        ast.Assign(
            targets=[ast.Name(id='gen_r_texts')],
            value=ast.Call(args=args, keywords=keywords, func=ast.Name(id='GetCourse')),
        ),
        ast.Return(value=ast.Name(id='gen_r_texts')),
    ])

    #  Вынимаем ФАСИФ глагола - сказуемого
    args_func_common = [ast.Name(id='arg0'), ast.Name(id='gen_r_texts')]
    id_group, str_func_common = utils.get_func_common(relation, predicate['base'], settings)
    if str_func_common:
        str_module, str_func_common = str_func_common.split(':')
        body.append(ast.ImportFrom(module=str_module, level=0, names=[ast.alias(name=str_func_common, asname=None)]))
        body.append(
            ast.Assign(
                targets=[ast.Name(id='gen_r_texts')],
                value=ast.Call(args=args_func_common, keywords=[], func=ast.Name(id=str_func_common)),
            )
        )

    module = build_main_tree(body)
    code = astor.to_source(module)
    return code


def analyze(message):
    relation = Relation(message.settings)
    internal_sentences = []
    for sentence in message.text:
        subjects_by_predicate, predicates, arguments_by_predicate = sentence
        for subjects, predicate, arguments in zip(subjects_by_predicate, predicates, arguments_by_predicate):
            internal_sentences.append(Extraction2IL(relation, message.settings, subjects, predicate, arguments))
            print(internal_sentences[-1])

    return '\n\n'.join(internal_sentences)
