import time
from manspy.analyzers import esperanto_morphological, executor_internal_sentences, converter, esperanto_syntax, esperanto_graphemathic, esperanto_postmorphological, extractor

all_levels = ["graphmath", "morph", "postmorph", "synt", "extract", "convert", "exec"]

level_to_analyzer = {
    "graphmath": esperanto_graphemathic,
    "morph": esperanto_morphological,
    "postmorph": esperanto_postmorphological,
    "synt": esperanto_syntax,
    "extract": extractor,
    "convert": converter,
    "exec": executor_internal_sentences,
}


class PipelinerGetter(list):
    def __init__(self, analyzers_list):
        super().__init__()
        self.names = []
        for name, analyzer in analyzers_list:
            self.append(analyzer)
            self.names.append(name)

    def __getitem__(self, index):
        if isinstance(index, str):
            start_name, end_name = index.split(':')
            start_index = self.names.index(start_name) if start_name else 0
            end_index = self.names.index(end_name) + 1 if end_name else len(self)
            return super().__getitem__(slice(start_index, end_index))

        return super().__getitem__(index)


def pipeliner(msg, analyzers=None):
    """ Второй аргумент - диапазон конвертирования от первого до последнего
        включительно через пробел. Если требуется сделать лишь один уровень,
        то можно указать только одно слово. Если указан только 'convert',
        то в качестве первого аргумента передаётся список извлечений."""
    if msg.settings.print_time:
        print('\n---------------------------------------')
        print('----', msg.text)
        print('---------------------------------------')
    t1 = time.time()

    msg.before_analyzes()

    if analyzers:
        for analyzer in analyzers:
            level = analyzer.__name__
            msg.before_analysis(level)
            t = time.time()

            msg.text = analyzer.analyze(msg)

            msg.analysis[level] = msg.text
            msg.after_analysis(level, msg.text)
            if msg.settings.print_time:
                print('   '+level.rjust(9)+': ', time.time()-t)
    else:
        levels = msg.settings.levels.replace(' ', ':')
        start_level, end_level = levels.split(':')
        start_level = start_level if start_level else all_levels[0]
        end_level = end_level if end_level else all_levels[-1]

        for level in all_levels[all_levels.index(start_level):all_levels.index(end_level)+1]:
            msg.before_analysis(level)
            t = time.time()

            analyzer = level_to_analyzer[level]
            msg.text = analyzer.analyze(msg)

            msg.analysis[level] = msg.text
            msg.after_analysis(level, msg.text)
            if msg.settings.print_time:
                print('   '+level.rjust(9)+': ', time.time()-t)

    msg.time_total = time.time() - t1
    if msg.settings.print_time:
        print('       Total: ', msg.time_total)

    return msg.text