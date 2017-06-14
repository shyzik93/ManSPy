def getLangModule(language):
    return __import__(language, globals=globals(), level=1)