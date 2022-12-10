# TODO: Добавить модуль xmp в requirements.txt
from manspy.runners.simple import runner


class Interface:
    def __init__(self, settings, config):
        self.settings = settings
        settings.send_to_out = self.send_to_out
        self.config = config

    def FromUser(self, conn, messR):
        w_text = messR.getBody()
        From = str(messR.getFrom()).split('/')[0]

        if w_text:
            runner(w_text, self.settings, any_data=From)

    def send_to_out(self, r_text, From):
        if From:
            self.bot.send(xmpp.Message(From, r_text))

    def init(self):
        login = self.config['login']
        password = self.config['pass']
        jid = xmpp.JID(login)
        bot = xmpp.Client(jid.getDomain(), debug=[])
        # авторизация и запуск Jabber
        bot.connect()
        bot.auth(jid.getNode(), password, resource="Python Jabber Bot")
        bot.RegisterHandler('message', self.FromUser)

        prs=xmpp.Presence(priority=100, show='dnd')
        prs.setStatus(u"Мой бот. Цель - проверка некоторых алгоритмов")
        bot.send(prs)

        bot.online = 1
        while bot.online:
            self.bot = bot
            bot.Process(1)

        bot.disconnect()
        print("Отключено :(")
