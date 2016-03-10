class ObjRelation(object):
  def __init__(self, language, test=0, version=1):
    self.OR = __import__('relation_v'+str(version), globals={"__name__":__name__})._ObjRelation(language, test)
  def __getattr__(self, name):
    return self.OR.__getattribute__(name)
