""" В скобках после ответа показано количество ответов, которое ИСУ вам покажет
    после нажатия на Enter, то есть при отправке пустого сообщения :)
"""
import time


class Interface:
    def __init__(self, api, settings, config):
        self.api = api
        self.settings = settings(read_text=self.read_text)

    def read_text(self, r_text, any_data):
        print(r_text)

    def init(self):
        while 1:
            w_text = input()
            if w_text == '\\exit':
                exit(0)
            self.api.write_text(w_text, self.settings)
            #time.sleep(0.01)
