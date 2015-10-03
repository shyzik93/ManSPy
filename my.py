# -*- coding: utf-8 -*-

def match_dicts(dict1, dict2, level=0):
  ''' Показывает отличия dict2 от dict1 '''
  keys1 = dict1.keys()
  keys2 = dict2.keys()
  keys = list(set(keys1 + keys2))
  absent = []
  added = []

  for key in keys:
    if key in keys1 and key in keys2:
      if dict1[key] != dict2[key]:
        print 'key:', key
        print 'values:\n', '  ', dict1[key], '\n  ', dict2[key], '\n'
      if 'dict' in str(type(dict1[key])):
        print '--'*level*2, key
        match_dicts(dict1[key], dict2[key], level+1)
    elif key not in keys1 and key in keys2: added.append(key)
    elif key in keys1 and key not in keys2: absent.append(key)

  print 'absent:', absent
  print 'added:', added
  print ''

old = {'function': ('CurrencyLoader', 'GetCourse'), 'arguments_description': {0: {'case': 'genetive', 'parentMOSentence': 'direct supplement', 'required': 1, 'POSpeech': 'noun', 'MOSentence': 'supplement', 'base': u'bank', 'parentBase': u'cambi'}, 'currency': {'case': 'accusative', 'parentMOSentence': 'direct supplement', 'argtable': {u'rubl': 'RUB', u'grivn': 'UAH', u'dolar': 'USD', u'e\u016dr': 'EUR'}, 'required': 1, 'POSpeech': 'adjective', 'parentCase': 'accusative', 'parentBase': u'cambi', 'base': [u'moner'], 'MOSentence': 'definition'}, 'country': {'case': 'nominative', 'parentMOSentence': 'supplement', 'argtable': {u'rusi': 'Russia', u'ukraini': 'Ukraine', u'belarusi': 'Belarus'}, 'required': 0, 'POSpeech': 'adjective', 'parentCase': 'genetive', 'parentBase': u'bank', 'base': [u'land'], 'parentLink': 0, 'MOSentence': 'definition'}}}
new = {'function': ['CurrencyLoader', u'GetCourse'], 'arguments_description': {0: {'case': 'genetive', 'parentMOSentence': 'direct supplement', 'required': 1, 'POSpeech': 'noun', 'MOSentence': 'supplement', 'base': u'bank', 'parentBase': u'cambi'}, u'currency': {'case': 'accusative', 'parentMOSentence': 'direct supplement', 'argtable': {u'rubl': u'RUB', u'grivn': u'UAH', u'dolar': u'USD', u'e\u016dr': u'EUR'}, 'required': True, 'POSpeech': 'adjective', 'parentCase': 'accusative', 'parentBase': u'cambi', 'base': [u'moner'], 'MOSentence': 'definition'}, u'country': {'case': 'nominative', 'parentMOSentence': 'supplement', 'argtable': {u'rusi': u'Russia', u'ukraini': u'Ukraine', u'belarusi': u'Belarus'}, 'required': False, 'POSpeech': 'adjective', 'parentCase': 'genetive', 'parentBase': u'bank', 'base': [u'land'], 'parentLink': 0, 'MOSentence': 'definition'}}}
match_dicts(old['arguments_description'], new['arguments_description'])


'''class Modulo():
  def __init__(self, var):
    self.var = var
  def __mod__(self, M):
    return self.var * M.var

n1 = Modulo(6)
n2 = Modulo(8)

#print n1 % n2
print n1 % n2

n = 7
print n.bit_length()

def f(a, b=9):
  c = 5
  print b + c

print dir(f.func_code)

print f.func_code.co_lnotab
print [ord(i) for i in f.func_code.co_code]'''

"""import threading

def a(index):
  print 'a', index
  print 'next'
def b(index):
  print 'b', index
  while index < 10:
    index +=1
    print index
  print 'next'
def c(index):
  print 'c', index
  print 'next'

func = [a, b, c]

index = 0
process = []

for i in range(len(func)):
  p = threading.Thread(target=func[i], args=(index,))
  #p.start()
  process.append(p)

print '-----------------------------------'

for p in process:
  p.start()"""

"""for p in process:
  p.start()
"""
