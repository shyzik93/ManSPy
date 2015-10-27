import relation_v1, relation_v2

class ObjRelation(object):
  ORs = {1: relation_v1._ObjRelation, 2: relation_v2._ObjRelation}
  def __init__(self, language, test=0, version=1):
    self.OR = self.ORs[version](language, test)
  def __getattr__(self, name):
    return self.OR.__getattribute__(name)
