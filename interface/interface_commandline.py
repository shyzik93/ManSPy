""" В скобках после ответа показано количество ответов, которое ИСУ вам покажет
    после нажатия на Enter, то есть при отправке пустого сообщения :)
"""
from manspy.runners.simple import runner


class Interface:
    def __init__(self, settings, config):
        self.settings = settings
        settings.send_to_out = self.send_to_out

    def send_to_out(self, r_text, any_data):
        print(r_text)

    def init(self):
        while 1:
            w_text = input()
            if w_text == '\\exit':
                exit(0)

            runner(w_text, self.settings)
            #time.sleep(0.01)
