class ImportAction(object):
  def __init__(self, settings, version=2):
    print 1
    self.OR = __import__('import_action_assoc'+str(version)).kImportAction(settings)
  def __getattr__(self, name):
    return self.OR.__getattribute__(name)
