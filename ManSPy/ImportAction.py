# -*- coding: utf-8 -*-

class ImportAction(object):
  def __init__(self, settings):
    self.OR = __import__('import_action_assoc'+str(settings['assoc_version']), globals={"__name__":__name__}).ImportAction(settings)
    #self.OR = __import__('import_action_assoc'+str(version)).ImportAction(settings)
  def __getattr__(self, name):
    #return getattr(self.OR, name) # работает в обоих случаях
    return self.OR.__getattribute__(name) # работает только с классами нового стиля (наследуемые от object)
