class ObjRelation(object):
    def __init__(self, settings, version=1):
        self.OR = __import__('relation_v'+str(version), globals={"__name__":__name__}, level=1)._ObjRelation(settings)
    def __getattr__(self, name):
        return self.OR.__getattribute__(name)
