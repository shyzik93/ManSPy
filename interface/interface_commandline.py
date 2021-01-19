""" В скобках после ответа показано количество ответов, которое ИСУ вам покажет
    после нажатия на Enter, то есть при отправке пустого сообщения :)
"""
import time


class Interface:
    def __init__(self, api, settings, config):
        self.api = api
        self.settings = settings(send_to_out=self.send_to_out)

    def send_to_out(self, r_text, any_data):
        print(r_text)

    def init(self):
        while 1:
            w_text = input()
            if w_text == '\\exit':
                exit(0)
            self.api.send_to_in(w_text, self.settings)
            #time.sleep(0.01)
