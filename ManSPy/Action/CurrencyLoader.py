#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ra93POL
# Date: 2014.06.01 - 2014.07.17
'''
 Модули для lxml
 cssselect: https://codeload.github.com/SimonSapin/cssselect/zip/master
            https://github.com/SimonSapin/cssselect/

 Собранный установщик lxml для Виндовс: http://www.lfd.uci.edu/~gohlke/pythonlibs/
'''

import lxml.html as html, urllib, re, datetime

crc_cnr = {
  'RUB': 'Russia',
  'BYR': 'Belarus',
  'UAH': 'Ukraine'
  }


# Прямой забор данных с сайтов Центральных Банков. Входное значение - имя государства.
# Возвращает словарь с валютами:
#   {Символьный код: [значение, номинал, наименование]}
def GetPricesFromCB(country):
  now = datetime.datetime.now()
  FullPrices = {}
  if country == 'Russia_old':
    page = html.parse('http://cbr.ru').getroot()
    div = page.cssselect('div#widget_exchange')[0]
    table = div.cssselect('table')[0]
    title = table.cssselect('td.title')
    weak = table.cssselect('td.weak')
    x = 0
    while x < len(title):
      key = title[x].text.strip()
      FullPrices[key] = weak[x].text.strip()
      x += 1
  if country == 'Russia':
    page = urllib.urlopen('http://www.cbr.ru/scripts/XML_daily.asp?date_req='+now.strftime('%d.%m.%Y')).read()
    page = page.replace('?xml', '') # убираем декларацию кодировки (с ней ругань)
    page = html.document_fromstring(page.decode('windows-1251'))
    valutes = page.cssselect('Valute')
    for v in valutes:
      CharCode = v.cssselect('CharCode').pop().text
      Value = v.cssselect('Value').pop().text
      Nominal = v.cssselect('Nominal').pop().text
      Name = v.cssselect('Name').pop().text
      FullPrices[CharCode] = [Value, Nominal, Name]
  elif country == 'Belarus':
    page = urllib.urlopen('http://www.nbrb.by/Services/XmlExRates.aspx?ondate='+now.strftime('%m/%d/%Y')).read()
    page = page.replace('?xml', '') # убираем декларацию кодировки (с ней ругань)
    page = html.document_fromstring(page.decode('utf-8'))
    valutes = page.cssselect('Currency')
    for v in valutes:
      CharCode = v.cssselect('CharCode').pop().text
      Value = v.cssselect('Rate').pop().text
      Nominal = v.cssselect('Scale').pop().text
      Name = v.cssselect('Name').pop().text
      FullPrices[CharCode] = [Value, Nominal, Name]
  elif country == 'Ukraine':
    page = urllib.urlopen('http://www.bank.gov.ua/control/uk/curmetal/detail/currency?period=daily').read()
    page = html.document_fromstring(page.decode('utf-8'))
    content = page.cssselect('div.content')[0]
    table = content.cssselect('table')[3]
    tr = table.cssselect('tr')
    del tr[0]
    for i in tr:
      td = i.cssselect('td')
      FullPrices[td[1].text] = [td[4].text, td[2].text, td[3].text]
  elif country == 'Georgia':
    page = urllib.urlopen('http://www.nbg.ge/rss.php').read()
    page = page.replace('?xml', '') # убираем декларацию кодировки (с ней ругань)
    page = html.document_fromstring(page.decode('utf-8'))
    valutes = page.cssselect('description')
    valutes = valutes[1].cssselect('tr')
    for v in valutes:
      v = v.cssselect('td')
      l = []
      for val in v:l.append(val.text)
      Nominal = re.findall(r'[0-9]*', l[1])[0]
      FullPrices[l[0]] = [l[2], Nominal, l[1][len(Nominal)+1:]]
  return FullPrices

# Преобразовывает словарь валют
# из {Символьный код: [значение, номинал, наименование]}
# в {Символьный код: значение}
def TransformPrices(FullPrices):
  ShortPrices = {}
  keys = FullPrices.keys()
  for key in keys:
    value = float(FullPrices[key][0].replace(',', '.')) / float(FullPrices[key][1]) 
    ShortPrices[key] = str(value)
  return ShortPrices 

def GetCourse(arg0, currency, country='Russia'):
  ''' Возвращает стоимость иностр. валюты в гос. валюте '''
  FullPrices = GetPricesFromCB(country)
  #print FullPrices
  ShortPrices = TransformPrices(FullPrices)
  if currency == 'all':
    res = ''
    x = 1
    keys = ShortPrices.keys()
    keys.sort()
    for key in keys:
      res_str = key +': '+ ShortPrices[key]
      if x%4 == 0: res_str += '\n'
      else: res_str += ' '*(20-len(res_str))
      res += res_str
      x += 1
    return res
  else:
    price = float(ShortPrices[str(currency)])
    print currency, country, price
    return price
# Выражение курса через другие валюты

def Convert(value, currency_from, currency_to, country):
  ''' Конвертирует единцы из валюты1 в валюту2. '''
  course = GetCourse(None, currency_from, crc_cnr[currency_to])
  return value * course

if __name__ == '__main__':
  def print_beauty_all():
    countries = ['Georgia', 'Russia', 'Belarus', 'Ukraine']
    for country in countries:
      print '\n', ' '*35, country.upper(), '\n'
      print GetCourse(None, 'all', country)
  #print Chain('USD', 'Ukraine', )
  print Convert(25, 'USD', 'RUB', 'Russia')
  print_beauty_all()

list_FASIF = ['''
# Описание Функции
GetCourse
currency y ;  Esperanto
# пробелы в начале строки обязательны
  USD      ;  dolar
  RUB      ;  rubl
  EUR      ;  eŭr
  UAH      ;  grivn
country n ;  Esperanto
  Russia  ;  rusi
  Belarus ;  belarusi
  Ukraine ;  ukraini
#argument n - если не требуется замена значения аргумента

# Шаблоны ЯЕ-предложений
Esperanto
dolaran: monero # аргументное слова: абстрактные группы через запятую
rusia: lando
montru dolaran cambion de rusia banko

Russian
доллара, валюта
русскому, страна, национальность
покажи курс доллара согласно русскому банку
''']
# montru dolaran cambion de mango de rusia banko
