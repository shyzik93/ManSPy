class FASIF:
    def __init__(self, lang_class):
        self.LangClass = lang_class

    def get_dword(self, word, settings):
        text = self.LangClass.NL2IL(word, settings, {'levels': ':postmorph', 'print_time': False})
        return list(text(0).getUnit('dict').values())[0]

    def proccess_argword(self, argwords, settings):
        argwords['name'] = self.get_dword(argwords['name'], settings)
        for index, argword in enumerate(argwords['hyperonyms']):
            argwords['hyperonyms'][index] = self.get_dword(argword, settings)
