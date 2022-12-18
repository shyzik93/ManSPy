import importlib
import pkgutil


def import_modules(path_import, module_type):
    for module_info in pkgutil.iter_modules(path=[path_import]):
        if module_info.name.startswith('{}_'.format(module_type)):
            try:
                module = module_info.module_finder.find_module(module_info.name).load_module()
            except Exception as e:
                print('Не удалось импортировать модуль "{}" в директории "{}"'.format(module_info.name, path_import))
                continue
            module_code = module_info.name
            yield module, module_code[len(module_type)+1:]


def import_action(string_import):
    # TODO: Использование встроенных действий: if function_str[0] == '$': return function_str[1:]
    module_name, callable_name = string_import.split(':')
    module_obj = importlib.import_module(module_name)
    return getattr(module_obj, callable_name)
