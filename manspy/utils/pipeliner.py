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


def pipeliner(message, analyzers=None):
    """ Второй аргумент - диапазон конвертирования от первого до последнего
        включительно через пробел. Если требуется сделать лишь один уровень,
        то можно указать только одно слово. Если указан только 'convert',
        то в качестве первого аргумента передаётся список извлечений."""
    message.before_analyzes(analyzers)
    for analyzer in analyzers:
        analyzer_name = analyzer.__name__
        message.before_analysis(analyzer_name)
        message.text = analyzer.analyze(message)
        message.analysis[analyzer_name] = message.text
        message.after_analysis(analyzer_name, message.text)

    message.after_analyzes(analyzers)
    return message.text
