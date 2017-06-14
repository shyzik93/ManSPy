import os, sys

_path = os.path.dirname(__file__)
sys.path.append(_path)

def getObject(module_name, object_name):
    module = __import__(module_name)
    if object_name in dir(module):
        return getattr(module, object_name)

def getModule(module_name):
    return __import__(module_name)
