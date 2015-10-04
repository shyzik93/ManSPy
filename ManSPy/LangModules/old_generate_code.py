# -*- coding: utf-8 -*-
import re

input_vars = {  'id_type': '_type',
              'id_speech': 'speech',
                'id_word': 'word',
               'id_words': 'words',
                'pairs': 'pairs'
                }
output_vars = {}
for k, v in input_vars.items(): output_vars[v] = k
convert_input_vars = { '_type': 'id_type = self.id_types[%s]',
                   'speech': 'id_speech = self.id_speeches[%s]',
                   '*words': 'id_words = _Relation.word_to_id(%s)',
                     'word': 'id_word = _Relation._word_to_id(%s)',
                   '*pairs': 'for pair in pairs: pair[0] = _Relation._word_to_id(pair[0]) #%s'
                   }
convert_output_vars = { 'id_type': '_type = self.id_types_reverse[%s]',
                   #'id_speech': 'speech = self.id_speeches_reverse[%s]',
                   'id_words': 'words = _Relation.id_to_word(*%s)',
                     'id_word': 'word = _Relation._id_to_word(%s)'
                   }
except_func = ['__init__', 'add_word', 'id_to_word', '_id_to_word', '_word_to_id', 'word_to_id', 'get_max_id']

class_for_recostruction = '_Relation'
functions = []
count_spaces = 2

spaces = ' '*count_spaces
level = 0

with open('Relation_new.py', 'r') as f:
  code = f.read().split('\n')

print 'all strings:', len(code)
i = 0
while i < len(code):
  if not code[i]:
    del code[i]
    continue
  i += 1
print 'without empty strings:', len(code), '\n'

def get_level(s):
  #print re.findall('^ *', s)
  c_spaces = float(len(re.findall('^ *', s)[0]))
  if c_spaces % count_spaces != 0: print u'Неправильный отступ!', s
  return c_spaces/count_spaces

def get_name_args(_s, construction):
  l = len(construction)
  s = _s[l:].strip().replace('):', '').split('(', 1)
  if len(s)==2: name, args = s
  elif len(s)==1:
    name = s[0]
    args = ''
  name = name.strip()
  args = [arg.strip() for arg in args.split(',') if arg]
  print name, args
  return name, args

def proccess_function(start_level, code, start_i):
  s = code[start_i].strip()
  name, args = get_name_args(s, 'def')
  if name in except_func: return

  function = {'name': name, 'args': args}
  ret = []
  level = start_level+1 # +1 - чтобы запустился цикл
  i = start_i
  while level > start_level:
    i += 1
    if len(code) == i: break
    s = code[i]
    level = get_level(s)
    s = s.strip()
    if re.findall('^return', s) or re.findall(': ?return', s):
      s = s.split('return')[1]
      s = s.split('#FORAUTO')[-1]
      s = [_s.strip() for _s in s.split(',') if _s]
      ret.append(s)
  if ret: print ret
  function['rets'] = ret
  functions.append(function)
  print

def proccess_class(start_level, code, start_i):
  s = code[start_i].strip()
  name, args = get_name_args(s, 'class')

  if name != class_for_recostruction: return
  level = start_level+1 # +1 - чтобы запустился цикл
  i = start_i
  while level > start_level:
    i += 1
    if len(code) == i: break
    s = code[i]
    level = get_level(s)
    s = s.strip()
    if len(s)>3 and level == start_level+1 and s.split(' ')[0] == 'def':
      proccess_function(level, code, i)

i = -1
while i < len(code)-1:
  i += 1
  s = code[i]
  level = get_level(s)
  s = s.strip()
  if len(s)>5 and level == 0 and s.split(' ')[0] == 'class':
    proccess_class(level, code, i)


new_code = []
names = {'idword': 'word', 'idgroup': 'group', 'idtype': 'type'}
for function in functions:
  full_args = function['args']
  print function['rets']
  if len(function['rets']): function['rets']= function['rets'][0]

  input_args = [] # только имена
  for full_arg in full_args: input_args.append(full_arg.split('=')[0])
  output_args = [] # только имена
  for full_arg in function['rets']: output_args.append(full_arg)

  _new_code = []
  for full_arg in full_args:
    for key in input_vars.keys():
      if re.findall(r'\*?'+key+'$', full_arg):
        convert_arg = full_arg.replace(key, input_vars[key])
        print function['name'], full_args, full_arg
        full_args[full_args.index(full_arg)] = convert_arg
        convert_arg = convert_arg.split('=')[0]
        if convert_arg in convert_input_vars: _new_code.append('    ' + convert_input_vars[convert_arg] % convert_arg)
  name = function['name']
  for name1, name2 in names.items(): name = name.replace(name1, name2)
  s = '  def %s(%s):' % (name[1:], ', '.join(full_args))
  new_code.append(s)
  new_code.extend(_new_code)
  # генерируем строку вызова функции (возвращенеи аргументов)
  if output_args: assignment_symbol = ', '.join(output_args) + ' = '
  else: assignment_symbol = ''
  for output_arg in output_args:
    if output_arg in ['True', 'False']: assignment_symbol = 'return '
  new_code.append('    '+assignment_symbol+'Relation.'+ function['name']+'(' +', '.join(input_args)+ ')')

  # генерируем возвращаемые переменные
  for output_arg in output_args:
    if output_arg in convert_output_vars.keys():
       convert_arg = convert_output_vars[output_arg] % output_arg
       new_code.append('    '+convert_arg)
       output_args[output_args.index(output_arg)] = input_vars[output_arg.replace('*', '')]
  if '=' in assignment_symbol: new_code.append('    return '+', '.join(output_args))

  new_code.append('')

with open('Relation_generated.py', 'w') as f:
  header ="""# -*- coding: utf-8 -*-
from Relation_new import _Relation

class Relation(_Relation):
  dct_types = {'synonym': 0, 'antonym': 1, 'abstract': 2}
  dct_speeches = {'noun': 0, 'verb': 1, 'adjective': 2, 'adverb': 3}
  def __init__(self, language):
    _Relation.__init__(self, language)

"""
  f.write(header)
  for s in new_code: f.write(s+'\n')
  footer = """if __name__ == '__main__':
  R = Relation('Esperanto')
  R.add_word('montr', 'rubl')
  print R.id_to_word(1, 2)
"""
  f.write(footer)
