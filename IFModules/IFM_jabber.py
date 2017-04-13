# -*- coding: utf-8 -*-
import xmpp, os, sys, codecs

API = IFName = passwords = None
bot = None
white_list = ['ra93pol@jabber.ru']

class Interface():
  def __init__(self, API):
    self.API = API

  def FromUser(self, conn, messR):
    w_text = messR.getBody()
    From = str(messR.getFrom()).split('/')[0]

    if w_text == None: return
    if From not in white_list: r_text = 'Denied!'
    else:
      if w_text: self.API.write_text(self, w_text)

    self.To = From
    self.ToUser(From)

  def ToUser(self, To):
    while 1:
      r_text = self.API.read_text(self, -1)
      if To and r_text:
        self.bot.send(xmpp.Message(To, r_text))

  def to_IF(self, r_text):
    if self.To:
      self.bot.send(xmpp.Message(To, r_text))

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
