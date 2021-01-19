from manspy.message import Message
from manspy.analyse_text import nature2internal


class FASIF:
    def get_dword(self, word, settings):
        levels = settings.levels
        settings.levels = ':postmorph'
        message = Message(settings, {}, word, 'W')
        text = nature2internal(message)
        settings.levels = levels
        return list(text(0).getUnit('dict').values())[0]

    def proccess_argword(self, argwords, settings):
        argwords['name'] = self.get_dword(argwords['name'], settings)
        for index, argword in enumerate(argwords['hyperonyms']):
            argwords['hyperonyms'][index] = self.get_dword(argword, settings)
