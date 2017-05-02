# -*- coding: utf-8 -*-
''' Модуль вспомогательный. Сохраняет результаты анализов для последующего
    выявления ошибок и неточностей.
'''
import os, datetime
from pprint import pprint

def fwrite(data, name='analysis.txt'):
    if not os.path.exists(name):
        f = open(name, 'w')
        f.close()
    with open(name, 'a', encoding='utf-8') as f:
        f.write(data)
        f.close()

def safeUnknown(list_res):
    ''' запись нераспознанных слов ??????????'''
    l = []
    for res in list_res:
        #if res.has_key('POSpeech') == 0:
        #if len(res) == 1:
        if res['POSpeech'] == '':
            l.append(res['word'])
    index = 0
    while index < len(l):
        if l.count(l[index]) > 1: del l[index]
        index += 1
    t = ''
    for word in l: t += word + ' '
    fwrite(u'Нераспознанные слова: ' + t + u'\n\n')
    #f.close()
