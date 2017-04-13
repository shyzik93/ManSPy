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
    arg0['to_IF'](condition)

''' Состояние числительных '''
def get(arg0, a): return a

def _is_only_numbers(numbers):
  for i in numbers:
    if not isinstance(numbers, (int, float, complex)):
      return False
  return True

def add(arg0, *a):
  ''' Сложение '''
  a = list(a)

  if len(a) == 0: return 0

  if _is_only_numbers(a):

    start = a.pop(0)
    if arg0['antonym']:
      a = [-i for i in a]
    return sum(a, start)
  
  else:

    for index, i in enumerate(a): a[index] = str(a[index])
    if arg0['antonym']: return ' - '.join(a)
    return ' + '.join(a)

def multiply(arg0, *a):
  ''' Умножение '''
  a = list(a)

  if len(a) == 0: return 0

  if _is_only_numbers(a):

    res = float(a.pop(0))
    if arg0['antonym']:
      for i in a: res /= i
    else:
      for i in a: res *= i
    return res

  else:

    for index, i in enumerate(a): a[index] = str(a[index])
    if arg0['antonym']: return ' / '.join(a)
    return ' * '.join(a)