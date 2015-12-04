# -*- coding: utf-8 -*-

class ImportAction(object):
  def __init__(self, settings, version=2):
    self.OR = __import__('import_action_assoc'+str(version), globals={"__name__":__name__}).ImportAction(settings)
    #self.OR = __import__('import_action_assoc'+str(version)).ImportAction(settings)
    print dir(self.OR)
  def __getattr__(self, name):
    #return getattr(self.OR, name) # работает в обоих случаях
    return self.OR.__getattribute__(name) # работает только с классами нового стиля (наследуемые от object)
