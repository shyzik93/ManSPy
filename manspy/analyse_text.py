import sys, os, time
from . import NLModules, relation, extractor, converter

class LangClass():

    levels = ["graphmath", "morph", "postmorph", "synt", "extract", "convert"]

    def __init__(self):
        self.lang_modules = {}

    def get_lang_module(self, language):
        if language not in self.lang_modules:
            #TODO проверить наличие модуля и наличие имён в нём
            self.lang_modules[language] = NLModules.getLangModule(language)

        return self.lang_modules[language]

    def parse_level_string(self, levels):
        ''' parsing level string. Return start_level, end_level. '''
        levels = levels.split()
        if len(levels)==1:
            level = levels.pop()
            if level[0] == ':': return self.levels[0], level[1:]
            elif level[-1] == ':': return level[:-1], self.levels[-1]
            return level, level
        return levels

    def NL2IL(self, msg, levels="graphmath convert", settings=None):
        """ Второй аргумент - диапазон конвертирования от первого до последнего
            включительно через пробел. Если требуется сделать лишь один уровень,
            то можно указать только одно слово. Если указан только 'convert',
            то в качестве первого аргумента передаётся список извлечений."""

        if settings is None:
            settings = msg.IF.settings
            sentences = msg.w_text
        else:
            sentences = msg
            msg = None

        print('\n---------------------------------------')
        print('----', sentences)
        print('---------------------------------------')
        t1 =time.time()

        if msg and msg.IF.settings['log_all']: msg.history.header(levels)

        OR = relation.ObjRelation(settings, settings['storage_version']) # не выносить в __init__! Объект работы с БД должен создаваться в том потоке, в котором и будет использован
        lang_module = self.get_lang_module(settings['language'])
        start_level, end_level = self.parse_level_string(levels)

        
        for i in range(self.levels.index(start_level)+1, len(self.levels)+1):
            t =time.time()

            if self.levels[i-1] == "graphmath": sentences = lang_module.getGraphmathA(sentences)
            elif self.levels[i-1] == "morph": sentences = lang_module.getMorphA(sentences)
            elif self.levels[i-1] == "postmorph": sentences = lang_module.getPostMorphA(sentences)
            elif self.levels[i-1] == "synt": sentences = lang_module.getSyntA(sentences)
            elif self.levels[i-1] == "extract":

                extractors = []
                Extract = extractor.Extract(settings['assoc_version'])
                for index, sentence in sentences:
                    OR.addWordsToDBFromDictSentence(sentence.getUnit('dict'))
                    extractors.append(Extract(sentence)) # заменяем объекты предложения на словари извлечений
                sentences = extractors

            elif self.levels[i-1] == "convert":

                OR = relation.ObjRelation(settings, settings['storage_version']) # не выносить в __init__! Объект работы с БД должен создаваться в том потоке, в котором и будет использован
                _ILs = {}
                for index, sentence in enumerate(sentences):
                    _ILs[index] = []
                    Extraction2IL = converter.Extraction2IL(settings['assoc_version'])
                    ILs = Extraction2IL(OR, settings, *sentence)
                    _ILs[index].extend(ILs)
                sentences = _ILs

            if msg and msg.IF.settings['log_all']: msg.history.log(self.levels[i-1], sentences)
            print('   '+self.levels[i-1].rjust(9)+': ', time.time()-t)
            if end_level == self.levels[i-1]:
                print('       Total: ', time.time()-t1)
                return sentences

    def IL2NL(self, IL):
        #IL = Synthesizer.IL2resultA(IL)
        #result = LangModule.ResultA2NL(IL)
        #return NL
        return IL
