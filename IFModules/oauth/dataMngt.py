# -*- coding: utf-8 -*-

def write(name, text, mode): # забросить в repper.py
    f = open(name, mode)
    f.write(text)
    f.close()

def write_list(name, list_text, shell_text='%s', key=None):
    f = open(name, 'a')
    for text in list_text:
        if key != None: text = text[key]
        f.write(shell_text % str(text))
    f.close()

def load_user_data():
    f = open('IFModules/oauth/user_data.txt', 'r')
    user_data = f.read()
    f.close()
    user_data = user_data.split(' ')

    return user_data
