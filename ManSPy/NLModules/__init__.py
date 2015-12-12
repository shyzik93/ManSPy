import ObjUnit

def getModule(language):
  return __import__(language, globals=globals())
  
