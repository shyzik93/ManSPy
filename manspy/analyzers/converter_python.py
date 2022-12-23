import ast

import astor

from manspy.analyzers.utils import get_func_common, get_func_wcomb
from manspy.storage.relation import Relation
from manspy.utils.unit import Sentence


def build_importfrom(str_import, body_imports):
    str_module, str_func = str_import.split(':')
    body_imports.append(
        ast.ImportFrom(module=str_module, level=0, names=[ast.alias(name=str_func, asname=None)]),
    )
    return str_func


def build_running_wcomb(str_func, finded_arg, body_func_wcomb):
    keywords = [
        ast.keyword(arg=key, value=ast.Constant(kind='', value=value))
        for key, value in finded_arg.items()
    ]
    body_func_wcomb.append(
        ast.For(
            target=ast.Name(id='r_text'),
            iter=ast.Call(
                args=[ast.Name(id='arg0')],
                keywords=keywords,
                func=ast.Name(id=str_func),
            ),
            body=[
                ast.Expr(
                    value=ast.Yield(
                        ast.Name(id='r_text'),
                    ),
                ),
            ],
            orelse=[],
        ),
    )

def Extraction2IL(relation, settings, subjects, predicate, arguments):
    body_imports = []
    body_func_wcomb_getters = []
    body_func_wcomb_setters = []
    body_func_common = None
    is_antonym = predicate['antonym']

    #  Вынимаем ФАСИФ глагола - сказуемого
    args_func_common = [ast.Name(id='arg0'), ast.Name(id='gen_r_texts')]
    verb_id_group, str_func_common = get_func_common(relation, predicate['base'], settings)
    if str_func_common:
        str_func_common = build_importfrom(str_func_common, body_imports)
        body_func_common = ast.Return(
            value=ast.Call(args=args_func_common, keywords=[], func=ast.Name(id=str_func_common)),
        )

    # Вынимаем Фасиф словосочетаний - актантов
    for _argument in arguments:  # у подпредложения может быть несколько актантов
        str_import_get_value, str_import_set_value, finded_args, finded_set_by_antonym = get_func_wcomb(Sentence(_argument), settings, relation, verb_id_group)
        if finded_args is not None:
            if str_import_get_value:
                str_func_get_value = build_importfrom(str_import_get_value, body_imports)
                for finded_arg in finded_args:
                    build_running_wcomb(str_func_get_value, finded_arg, body_func_wcomb_getters)

            if str_import_set_value:
                str_func_set_value = build_importfrom(str_import_set_value, body_imports)
                for finded_arg in finded_args:
                    build_running_wcomb(str_func_set_value, finded_arg, body_func_wcomb_setters)

            if finded_set_by_antonym:
                is_antonym = not is_antonym

    body_arg0 = ast.Assign(
        targets=[ast.Name(id='arg0')],
        value=ast.Dict(
            keys=[
                ast.Constant(kind='', value='answer_type'),
                ast.Constant(kind='', value='antonym'),
            ],
            values=[
                ast.Constant(kind='', value=settings.answer_type),
                ast.Constant(kind='', value=is_antonym),
            ]
        ),
    )

    body = [*body_imports, body_arg0]
    if body_func_common and body_func_wcomb_getters:
        body_func_wcomb_calling_def = ast.FunctionDef(
            body=body_func_wcomb_getters, name='run_wcomb', decorator_list=[],
            args=ast.arguments(args=[], defaults=[], vararg=None, kwarg=None)
        )
        body_func_wcomb_calling_call = ast.Assign(
            targets=[ast.Name(id='gen_r_texts')],
            value=ast.Call(args=[], keywords={}, func=ast.Name(id='run_wcomb')),
        )
        body.append(body_func_wcomb_calling_def)
        body.append(body_func_wcomb_calling_call)
        body.append(body_func_common)
    elif not body_func_common and body_func_wcomb_setters:
        body.extend(body_func_wcomb_setters)

    module_body = [
        ast.FunctionDef(
            body=body,
            name='execute',
            decorator_list=[],
            args=ast.arguments(args=[], defaults=[], vararg=None, kwarg=None),
        ),
    ]
    code = astor.to_source(ast.Module(body=module_body))
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
