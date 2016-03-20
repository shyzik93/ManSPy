def getLangModule(language):
  return __import__(language, globals=globals())