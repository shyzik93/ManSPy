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


def language(path_import):
    for module_info in pkgutil.iter_modules(path=[path_import]):
        if module_info.name.startswith('language_'):
            module = module_info.module_finder.find_module(module_info.name).load_module()
            module_code = module_info.name
            yield module, module_code[9:]


def logger(path_import):
    for module_info in pkgutil.iter_modules(path=[path_import]):
        if module_info.name.startswith('logger_'):
            module = module_info.module_finder.find_module(module_info.name).load_module()
            module_code = module_info.name
            class_name = ''.join([subname.capitalize() for subname in module_code.split('_')])
            yield getattr(module, class_name)(), module_code[7:]


def action(function_str):
    #if function_str[0] == '$': return function_str[1:]
    func_name = os.path.basename(function_str)
    module_file = os.path.dirname(function_str)
    module_name = os.path.basename(module_file)
    #module_path = os.path.abspath(os.path.dirname(module_file))
    module_path = os.path.dirname(module_file)
    sys.path.insert(0, module_path)
    print(function_str, module_path, module_name)
    module_obj = importlib.import_module(module_name)
    del sys.path[0]
    return getattr(module_obj, func_name)
