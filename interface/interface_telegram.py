import sys
import os.path

tg_path = os.path.normpath(os.path.join(os.path.basename(__file__), '../../telegram/'))
sys.path.append(tg_path)

# TODO: Добавить модуль telegram в requirements.txt
import telegram

from manspy.utils.pipeliner import pipeliner
from manspy.utils.message import Message

class Interface:
    def __init__(self, settings, config):
        self.settings = settings
        settings.send_to_out = self.send_to_out
        self.config = config

    def FromUser(self, m, comm_name, args, text):
        w_text = text
        from_user = m['chat_id']

        if w_text == None:
            return
        if w_text:
            pipeliner(Message(self.settings, w_text, any_data=from_user))

    def send_to_out(self, r_text, from_user):
        print(r_text, from_user)
        if from_user:
            self.tg.send_message(from_user, r_text)

    def init(self):
        self.tg = telegram.TelegramBot(self.config['token'])

        commands = {
        }

        self.tg.run(commands, self.FromUser)
