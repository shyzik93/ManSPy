import time


class Logger:
    statistic = {}

    def __init__(self):
        pass

    def on_create_message(self, direction, w_text, message):
        pass

    def before_analyzes(self, levels, message):
        self.statistic[message.id] = {}
        self.statistic['time_start'] = time.time()
        print('\n---------------------------------------')
        print('----', levels)
        print('----', message.text)
        print('---------------------------------------')

    def before_analysis(self, level, message):
        self.statistic[message.id][f'time_start_{level}'] = time.time()

    def after_analysis(self, level, sentences, message):
        time_start = self.statistic[message.id][f'time_start_{level}']
        self.statistic[message.id][f'time_spended_{level}'] = time.time() - time_start

    def after_analyzes(self, levels, message):
        time_start = self.statistic[message.id]['time_start']
        self.statistic[message.id]['time_spended'] = time.time() - time_start

        print(self.statistic)

    def close(self):
        pass
