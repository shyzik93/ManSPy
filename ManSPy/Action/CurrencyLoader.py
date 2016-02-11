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


def parseStandartXML(FullPrices, url, coding, blockname, charcode, value, nominal, name):
  page = urllib.urlopen(url).read()
  page = page.replace('?xml', '') # убираем декларацию кодировки (с ней ругань)
  page = html.document_fromstring(page.decode(coding))
  valutes = page.cssselect(blockname)
  for v in valutes:
    CharCode = v.cssselect(charcode).pop().text
    Value = v.cssselect(value).pop().text
    Nominal = v.cssselect(nominal).pop().text
    Name = v.cssselect(name).pop().text
    FullPrices[CharCode] = [Value, Nominal, Name]

# Прямой забор данных с сайтов Центральных Банков. Входное значение - имя государства.
# Возвращает словарь с валютами:
#   {Символьный код: [значение, номинал, наименование]}
def GetPricesFromCB(country):
  now = datetime.datetime.now()
  FullPrices = {}
  if country == 'Russia':
    parseStandartXML(FullPrices, 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='+now.strftime('%d.%m.%Y'), 'windows-1251', 'Valute', 'CharCode', 'Value', 'Nominal', 'Name')
  elif country == 'Belarus':
    parseStandartXML(FullPrices, 'http://www.nbrb.by/Services/XmlExRates.aspx?ondate='+now.strftime('%m/%d/%Y'), 'utf-8', 'Currency', 'CharCode', 'Rate', 'Scale', 'Name')
  elif country == 'Tajikistan':
    parseStandartXML(FullPrices, 'http://www.nbt.tj/ru/kurs/export_xml.php?date='+now.strftime('%Y-%m-%d')+'&export=xmlout', 'utf-8', 'Valute', 'CharCode', 'Value', 'Nominal', 'Name')
  elif country == 'Israel':
    parseStandartXML(FullPrices, 'http://www.boi.org.il/currency.xml', 'utf-8', 'CURRENCY', 'CURRENCYCODE', 'RATE', 'UNIT', 'NAME')
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
  elif country == 'Uzbekistan':
    page = urllib.urlopen('http://www.nbu.com/exchange_rates').read()
    page = html.document_fromstring(page.decode('utf-8'))
    content = page.cssselect('div.exchangeRates')[0]
    table = content.cssselect('table')[0]
    tr = table.cssselect('tr')
    del tr[0]
    for i in tr:
      td = i.cssselect('td')
      if td[3].text: FullPrices[td[6].text] = [td[3].text, td[2].text.split()[0], td[1].text]
  elif country == 'Turkmenistan':
    page = urllib.urlopen('http://www.cbt.tm/kurs/kurs_today_ru.html').read()
    page = html.document_fromstring(page.decode('utf-8'))
    content = page.cssselect('div#content_today')[0]
    table = content.cssselect('table')[0]
    tr = table.cssselect('tr')
    del tr[0]
    for i in tr:
      td = i.cssselect('td')
      if not td[0].cssselect('img'): continue
      nominal = td[3].text.strip()
      if not nominal: nominal = 1
      charcode = td[0].cssselect('img')[0].get('title')
      FullPrices[charcode] = [td[4].text.strip(), nominal, td[1].text] # в td[2].text - ена в USD
  elif country == 'Kazakhstan':
    parseStandartXML(FullPrices, 'http://www.nationalbank.kz/rss/rates_all.xml', 'utf-8', 'item', 'title', 'description', 'quant', 'title')
  elif country == 'Kyrgyzstan': # Киргизия
    page = urllib.urlopen('http://www.nbkr.kg/XML/weekly.xml').read()
    page = page.replace('?xml', '') # убираем декларацию кодировки (с ней ругань)
    page = html.document_fromstring(page.decode('utf-8'))
    valutes = page.cssselect('Currency')
    for v in valutes:
      CharCode = v.get('isocode')
      Value = v.cssselect('Value').pop().text
      Nominal = v.cssselect('Nominal').pop().text
      Name = CharCode
      FullPrices[CharCode] = [Value, Nominal, Name]
  # Афганистан: http://dab.gov.af/en/DAB/currency
  # Пакистан: http://www.sbp.org.pk/RSS/index.asp
  # Индия https://www.rbi.org.in/scripts/ReferenceRateArchive.aspx
  # Непал (есть XML) http://www.nrb.org.np/detailexchrate.php?YY=&&MM=&&DD=&&YY1=&&MM1=&&DD1=
  # Бутан http://www.rma.org.bt/EXTERNALWEB/index.jsp
  # Бангладеш https://www.bb.org.bd/econdata/exchangerate.php#/
  # Мьянма (JSON) http://forex.cbm.gov.mm/index.php/api
  # Тайланд https://ru.wikipedia.org/wiki/%D0%91%D0%B0%D0%BD%D0%BA_%D0%A2%D0%B0%D0%B8%D0%BB%D0%B0%D0%BD%D0%B4%D0%B0
  # Малайзия https://ru.wikipedia.org/wiki/%D0%91%D0%B0%D0%BD%D0%BA_%D0%9D%D0%B5%D0%B3%D0%B0%D1%80%D0%B0_%D0%9C%D0%B0%D0%BB%D0%B0%D0%B9%D0%B7%D0%B8%D1%8F
  # Лаос http://www.bol.gov.la/upload_reference/opd/rate/allrate.php
  # Вьетнам   http://www.sbv.gov.vn/portal/faces/en/enpages/er?_afrLoop=8695648468683715&_afrWindowMode=0&_afrWindowId=null#%40%3F_afrWindowId%3Dnull%26_afrLoop%3D8695648468683715%26_afrWindowMode%3D0%26_adf.ctrl-state%3D6mkhyv1wh_86
  # Сингапур http://www.mas.gov.sg/
  # Бруней http://www.ambd.gov.bn/Home.aspx
  # Филиппины http://www.bsp.gov.ph/
  # Тайвань http://www.bot.com.tw/english/Pages/default.aspx
  # Камбоджи http://nbc.org.kh/english/index.php
  # Мальдивы http://www.mma.gov.mv/
  # Шри-ланка http://www.cbsl.gov.lk/htm/english/_cei/er/e_1.asp

  # Список ЦБ https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%86%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%B1%D0%B0%D0%BD%D0%BA%D0%BE%D0%B2
  #           https://en.wikipedia.org/wiki/List_of_central_banks
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
      res_str = key +' '+ ShortPrices[key]
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
    countries = ['Israel', 'Georgia', 'Russia', 'Belarus', 'Ukraine', 'Tajikistan', 'Uzbekistan', 'Turkmenistan', 'Kazakhstan', 'Kyrgyzstan']
    for country in countries:
      print '\n', ' '*35, country.upper(), '\n'
      print GetCourse(None, 'all', country)
  #print Chain('USD', 'Ukraine', )
  print Convert(25, 'USD', 'RUB', 'Russia')
  print_beauty_all()


  countries = ['Georgia', 'Russia', 'Belarus', 'Ukraine', 'Tajikistan']
  FullPrices = GetPricesFromCB(countries.pop(0))
  uniq = set(FullPrices.keys())
  for country in countries:
    FullPrices = GetPricesFromCB(country)
    uniq = uniq & set(FullPrices.keys())
  print uniq

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
