# -*- coding: utf-8 -*-
import xmpp, os, sys, codecs

passwords = None

class Interface():
    def __init__(self, API):
        self.API = API
        self.settings = {'read_text': self.read_text}

    def FromUser(self, conn, messR):
        w_text = messR.getBody()
        From = str(messR.getFrom()).split('/')[0]

        if w_text == None: return
        if w_text: self.API.write_text(w_text, self.settings, {'any_data':From})

    def read_text(self, r_text, From):
        if From:
            self.bot.send(xmpp.Message(From, r_text))

    def init(self):
        login = passwords['login']
        password = passwords['pass']
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
