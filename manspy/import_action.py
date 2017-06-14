# -*- coding: utf-8 -*-

class ImportAction(object):
    def __init__(self, LangClass, version):
        self.OR = __import__('import_action_assoc'+str(version), globals={"__name__":__name__}, level=1).ImportAction(LangClass)
        #self.OR = __import__('import_action_assoc'+str(version)).ImportAction(settings)
    def __getattr__(self, name):
        #return getattr(self.OR, name) # работает в обоих случаях
        return self.OR.__getattribute__(name) # работает только с классами нового стиля (наследуемые от object)