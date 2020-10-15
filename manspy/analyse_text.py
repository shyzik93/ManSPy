import time
from manspy import relation
from manspy.extractor import extract
from manspy.converter import convert
from manspy import FCModule


class LangClass:
    levels = ["graphmath", "morph", "postmorph", "synt", "extract", "convert", "exec"]

    def __init__(self):
        self.LogicShell = FCModule.LogicShell()

    def parse_level_string(self, levels):
        """ parsing level string. Return start_level, end_level. """
        levels = levels.split()
        if len(levels) == 1:
            level = levels.pop()
            if level[0] == ':':
                return self.levels[0], level[1:]
            elif level[-1] == ':':
                return level[:-1], self.levels[-1]
            return level, level
        return levels

    def NL2IL(self, msg, settings=None, text_settings=None):
        """ Второй аргумент - диапазон конвертирования от первого до последнего
            включительно через пробел. Если требуется сделать лишь один уровень,
            то можно указать только одно слово. Если указан только 'convert',
            то в качестве первого аргумента передаётся список извлечений."""

        if settings is None:
            settings = msg.settings
            sentences = msg.w_text
            text_settings = msg.text_settings
        else:
            sentences = msg
            msg = None

        if text_settings['print_time']:
            print('\n---------------------------------------')
            print('----', sentences)
            print('---------------------------------------')
        t1 = time.time()

        if msg:
            msg.before_analyzes()

        OR = relation.ObjRelation(settings.language, settings.storage_version) # не выносить в __init__! Объект работы с БД должен создаваться в том потоке, в котором и будет использован
        lang_module = settings.modules['language'][settings.language]
        start_level, end_level = self.parse_level_string(text_settings['levels'])

        for level in self.levels[self.levels.index(start_level) : self.levels.index(end_level)+1]:
            if msg:
                msg.before_analysis(level)

            t = time.time()

            if level == "graphmath":
                sentences = lang_module.getGraphmathA(sentences)
            elif level == "morph":
                sentences = lang_module.getMorphA(sentences)
            elif level == "postmorph":
                sentences = lang_module.getPostMorphA(sentences)
            elif level == "synt":
                sentences = lang_module.getSyntA(sentences)
            elif level == "extract":
                sentences = extract(sentences, OR)
            elif level == "convert":
                #OR = relation.ObjRelation(settings, settings['storage_version']) # не выносить в __init__! Объект работы с БД должен создаваться в том потоке, в котором и будет использован
                sentences = convert(sentences, OR, settings)
            elif level == "exec":
                sentences = self.LogicShell.execIL(sentences, msg.to_IF)  # возвращает ошибки выполнения

            if msg:
                msg.after_analysis(level, sentences)
            if text_settings['print_time']:
                print('   '+level.rjust(9)+': ', time.time()-t)

        time_total = time.time()-t1
        if msg:
            msg.time_total = time_total
        if text_settings['print_time']:
            print('       Total: ', time_total)
        return sentences

    # TODO: должна возвращать `msg` со строкой ответа
    def IL2NL(self, IL):
        #IL = Synthesizer.IL2resultA(IL)
        #result = LangModule.ResultA2NL(IL)
        #return NL
        return IL
