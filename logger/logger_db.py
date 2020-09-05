TEMPLATE_PLAIN_ROW = '* {direction}  {date_recieved}  {ifname}:  {indent}{text}\n'

class LoggerDb:
    file_name = 'history.html'

    def __init__(self):
        pass

    def log(self, direction, text, msg):
        pass

    def before_analyzes(self, levels, msg):
        pass

    def before_analysis(self, level, msg):
        pass

    def after_analysis(self, level, sentences, msg):
        pass
