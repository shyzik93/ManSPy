""" В скобках после ответа показано количество ответов, которое ИСУ вам покажет
    после нажатия на Enter, то есть при отправке пустого сообщения :)
"""
from manspy.analyse_text import nature2internal
from manspy.message import Message


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
            nature2internal(Message(self.settings, w_text))
            #time.sleep(0.01)
