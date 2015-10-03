# -*- coding: cp1251 -*-
import time, oauth

API = IFName = passwords = None

Oauth = None
safe_user_id = '275575214'

def ToUser():
  global API, IFName, safe_user_id
  r_text = API.read_text(IFName, -1)
  if r_text: oauth.vk_messagesSend(safe_user_id, r_text)

def FromUser():
  global API, IFName
  messages = oauth.vk_messagesGet(0, 10)
  if not messages:
    print 'something is wrong...'
    return

  messages = messages['items']
  for message in messages:
    w_text =  message['body']
    user_id =  message['user_id']
    read_state =  message['read_state']
    message_id =  message['id']

    if read_state == 0:
      oauth.vk_messagesMarkAsRead(message_id)
      oauth.vk_messagesSetActivity(user_id)
      API.write_text(IFName, w_text)
  time.sleep(1)

def init():
  global Oauth
  Oauth = oauth.authorize(passwords)
  Oauth.print_log = True
  while 1:
    ToUser()
    FromUser()
