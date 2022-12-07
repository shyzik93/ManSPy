import time
from analyzers import extractor, converter, executor_internal_sentences

all_levels = ["graphmath", "morph", "postmorph", "synt", "extract", "convert", "exec"]


def nature2internal(msg):
    """ Второй аргумент - диапазон конвертирования от первого до последнего
        включительно через пробел. Если требуется сделать лишь один уровень,
        то можно указать только одно слово. Если указан только 'convert',
        то в качестве первого аргумента передаётся список извлечений."""
    sentences = msg.text

    if msg.settings.print_time:
        print('\n---------------------------------------')
        print('----', sentences)
        print('---------------------------------------')
    t1 = time.time()

    msg.before_analyzes()

    lang_module = msg.settings.modules['language'].get(msg.settings.language)
    if lang_module is None:
        print('Языковой модуль "{}" не был импортирован. Анализ невозможен.'.format(msg.settings.language))
        return []

    levels = msg.settings.levels.replace(' ', ':')
    start_level, end_level = levels.split(':')
    start_level = start_level if start_level else all_levels[0]
    end_level = end_level if end_level else all_levels[-1]

    for level in all_levels[all_levels.index(start_level):all_levels.index(end_level)+1]:
        msg.before_analysis(level)
        t = time.time()

        if level == "graphmath":
            sentences = lang_module.analysis_graphemathic.analyze(sentences)
        elif level == "morph":
            sentences = lang_module.analysis_morphological.analyze(sentences)
        elif level == "postmorph":
            sentences = lang_module.analysis_postmorphological.analyze(sentences)
        elif level == "synt":
            sentences = lang_module.analysis_syntax.analyze(sentences)
        elif level == "extract":
            sentences = extractor.analyze(sentences)
        elif level == "convert":
            sentences = converter.analyze(sentences, msg.settings)
        elif level == "exec":
            sentences = executor_internal_sentences.analyze(sentences, msg.send_to_out)

        msg.analysis[level] = sentences
        msg.after_analysis(level, sentences)
        if msg.settings.print_time:
            print('   '+level.rjust(9)+': ', time.time()-t)

    msg.time_total = time.time() - t1
    if msg.settings.print_time:
        print('       Total: ', msg.time_total)

    return sentences
