import importlib


def import_action(string_import):
    # TODO: Использование встроенных действий: if function_str[0] == '$': return function_str[1:]
    module_name, callable_name = string_import.split(':')
    module_obj = importlib.import_module(module_name)
    return getattr(module_obj, callable_name)
