import time
from analyzers import extractor, converter, executor_internal_sentences
from analyzers import esperanto_graphemathic
from analyzers import esperanto_morphological
from analyzers import esperanto_postmorphological
from analyzers import esperanto_syntax

all_levels = ["graphmath", "morph", "postmorph", "synt", "extract", "convert", "exec"]


def nature2internal(msg):
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

    levels = msg.settings.levels.replace(' ', ':')
    start_level, end_level = levels.split(':')
    start_level = start_level if start_level else all_levels[0]
    end_level = end_level if end_level else all_levels[-1]

    for level in all_levels[all_levels.index(start_level):all_levels.index(end_level)+1]:
        msg.before_analysis(level)
        t = time.time()

        if level == "graphmath":
            msg.text = esperanto_graphemathic.analyze(msg)
        elif level == "morph":
            msg.text = esperanto_morphological.analyze(msg)
        elif level == "postmorph":
            msg.text = esperanto_postmorphological.analyze(msg)
        elif level == "synt":
            msg.text = esperanto_syntax.analyze(msg)
        elif level == "extract":
            msg.text = extractor.analyze(msg)
        elif level == "convert":
            msg.text = converter.analyze(msg)
        elif level == "exec":
            msg.text = executor_internal_sentences.analyze(msg)

        msg.analysis[level] = msg.text
        msg.after_analysis(level, msg.text)
        if msg.settings.print_time:
            print('   '+level.rjust(9)+': ', time.time()-t)

    msg.time_total = time.time() - t1
    if msg.settings.print_time:
        print('       Total: ', msg.time_total)

    return msg.text
