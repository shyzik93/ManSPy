# -*- coding: utf-8 -*-
import xmpp, os, sys, codecs

API = IFName = passwords = None

path = os.path.dirname(__file__) + '\\'
path_config = path + 'jabber.password'

# Загружаем логин и пароль
#f = open(path_config, 'r')
#login, password = f.read().split(' ')
#login, password = passwords
#f.close()
# Соединение
#jid = xmpp.JID(login)
bot = None#xmpp.Client(jid.getDomain(), debug=[])

white_list = ['ra93pol@jabber.ru']

From = None

def FromUser(conn, messR):
  global From
  w_text = messR.getBody()
  From = str(messR.getFrom()).split('/')[0]

  if w_text == None: return
  if From not in white_list: r_text = 'Denied!'
  else:
    if w_text: API.write_text(IFName, w_text)

  ToUser()

def ToUser():
  global From, bot
  while 1:
    r_text = API.read_text(IFName, -1)
    if From and r_text:
      bot.send(xmpp.Message(From, r_text))

def init():
  global API, IFName, bot
  login, password = passwords
  jid = xmpp.JID(login)
  bot = xmpp.Client(jid.getDomain(), debug=[])
  # авторизация и запуск Jabber
  bot.connect()
  bot.auth(jid.getNode(), password, resource="Python Jabber Bot")
  bot.RegisterHandler('message', FromUser)

  prs=xmpp.Presence(priority=100, show='dnd')
  prs.setStatus(u"Мой бот. Цель - проверка некоторых алгоритмов")
  bot.send(prs)

  bot.online = 1
  while bot.online:
    bot.Process(1)

  bot.disconnect()
  print "Отключено :("
