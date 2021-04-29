import importlib
import pkgutil
import sys
import os.path

# module_dir = self.paths_import['language']
# for module_file_name in os.listdir(module_dir):
#    if module_file_name.startswith('language_'):
#        module_path = os.path.join(module_dir, module_file_name)
#        module = importlib.import_module(module_path)
#        print(module)


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


def action(abs_path_to_function):
    # TODO: Использование встроенных действий: if function_str[0] == '$': return function_str[1:]
    func_name = os.path.basename(abs_path_to_function)
    module_file = os.path.dirname(abs_path_to_function)
    module_name = os.path.basename(module_file)
    module_path = os.path.dirname(module_file)
    sys.path.insert(0, module_path)
    module_obj = importlib.import_module(module_name)
    del sys.path[0]
    return getattr(module_obj, func_name)


def database(db_type):
    module = importlib.import_module('manspy.database_drivers')
    return getattr(module, 'get_{}'.format(db_type))
