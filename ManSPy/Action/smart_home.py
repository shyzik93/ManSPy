# -*- coding: utf-8 -*-

#Включи настольный свет в спальне.
#Запрос отсутствующего аргумента:
#-Включи свет в спальне. -Какой именно свет? -Настольный.

import socket
from urllib import request

def SmartHome(group, room, device, cond):
  url = "http://192.168.0.101/manage.php?to=" +group+ "%20" +room+ "%20" +device+ "&command=" +cond+ "&string=on"
  print(url)
  request.urlopen(url).read()

def LightOn(arg0, room, device):
  if arg0['antonym']: cond="0%200%200"
  else: cond="1%201%201"
  return cond
  #SmartHome("light", room, device, cond)

def showAddress(arg0, device):
  if arg0['antonym']: return
  if device == 'computer': return str(socket.gethostbyname(socket.getfqdn()))
  return device

def printToIF(arg0, *conditions):
  for condition in conditions:
    arg0['forread'].add2read(condition)

''' Состояние числсительных '''
def get(arg0, a): return a

def add(arg0, *a):
  ''' Сложение '''
  a = list(a)
  if arg0['antonym']:
    start = a.pop(0)
    a = [-i for i in a]
    return sum(a, start)
  return sum(a)

def multiply(arg0, *a):
  ''' Умножение '''
  a = list(a)
  res = float(a.pop(0))
  if arg0['antonym']:
    for i in a: res /= i
  else:
    for i in a: res *= i
  return res
