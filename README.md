<p align="center"><img src="https://raw.githubusercontent.com/shyzik93/manspy/master/manspy_logo3.png" style="width:200px;"></p>

<p align="center"><h1 align="center"> ManSPy: "Programmer! Please, make me smart!" </h1></p>

[![Build Status](https://travis-ci.com/shyzik93/ManSPy.svg?branch=master)](https://travis-ci.com/shyzik93/ManSPy)

- Язык программирования: Python 3.4
- Естественный язык: Esperanto (можно написать модуль для Вашего языка)

Ссылки:
- Этот файл - ознакомление с программой
- http://github.com/shyzik93/ManSPy/wiki - описание алгоритмов
- http://dosmth.ru/media/history_promo.html - история диалога с программой

## Краткая история диалога

<img src="https://raw.githubusercontent.com/shyzik93/manspy/master/history_promo.png">

# Поверхностный взгляд

Основная идея программы - попытка ответить на вопрос: Что максимального удастся сделать до привлечения искусственных нейронных сетей?

Основные принципы:
- *сбор максимальной информации о предложениях на естественном языке, то есть учёт максимального количества деталей в тексте.*
- *возможность восстановить исходное предложение на естественном языке из результатов лингвистических анализов: это должно обеспечить качественный анализ, а в будущем - помочь с синтезом текста.*
- *если в предложении присутствует двусмысленность, то программа должна задать уточняющий вопрос*

В идеальных преувеличенных планах:
- *экспертная система*
- *система управления (ассистент)*

Путь предложений на естественном языке в программе:
1. *Графематический анализ*
1. *Морфологический анализ*
1. *Постморфологический анализ*
1. *Синтаксический анализ*
1. *Разбивка предложения на подлежащее, сказуемое и актанты (словосочетания)*
1. *Преобразование во внутренний язык. Язык представлен массивом, содержащим функцию и аргументы.*
1. *Выполнение функции, которая может возвращать пользователю простой ответ.*

На данный момент реализована возможность выполнения функций при использовании простых предложений с прямым порядком слов, если глагол указан в повелительном наклонении. Программа умеет распозновать синонимы и антонимы глагола (в связи с чем в выполняемую функцию передаётся в первом аргументе соответствующее "уведомление", чтобы в одной функции реализовать сразу два противоположных действия) и других слов, если о них есть информация в базе данных (БД).

Программа построена с использованием принципа модульности, благодаря чему некоторые модули можно использовать отдельно от программы, а именно: модуль хранения семантических отношений, модуль лингвистического анализа текста на языке Эсперанто (реализованы графематический, морфологический и постморфологический, синтаксический анализы). А в модуле анализа доступен модуль с объектами единиц речи: объекты слова, предложения, текста, имеющие удобные функции для построения алгоритмов анализа.

## А как ManSPy можно использовать уже сейчас?

- лингвистический анализ текста на языке Эсперанто
- "подсвечивание" текстов на языке Эсперанто (например, в редакторах Sublime Text, Notepad++)
- конвертация числительных, прилагаьелные и существительные (производные от числительных) в число.
- Ваш вариант :)

# Дорожная карта

- [x] Поддержка числительных
- [x] Поддержка простых математических глаголов (сложение, умножение)
- [x] Отдельные настройки для каждого модуля интерфейса (МИ)
- [ ] Юнит-тесты для лингвистических модулей
- [ ] Поддержка конструкций в естественном языке - условий, циклов
- [ ] Примитивный синтез текста через подстановку ответа функции в текст вопроса
- [ ] Поддержка конструкций во внутреннем языке
- [ ] Возможность добавлять новые семантические отношения (антонимы, гиперонимы и прочее) через естественный язык
- [ ] Управление домом на примере трёхмерной модели

# Запуск

В программе используются следующие сторонние модули Python, которые необходимо устанавливать отдельно из-за их отсутствия в стандартной библиотеке:
- lxml - для парсинга страниц при авторизации во "ВКонтакте" и для парсинга страниц с курсами валют от ЦБ. (для ОС Windows: http://www.lfd.uci.edu/~gohlke/pythonlibs/)  
- cssselect - может проситься модулем lxml (https://codeload.github.com/SimonSapin/cssselect/zip/master, https://github.com/SimonSapin/cssselect/)
- xmpp - реализация протокола для jabber (http://xmpppy.sourceforge.net/, http://sourceforge.net/projects/xmpppy/files/, https://raw.githubusercontent.com/freebsd/freebsd-ports/master/net-im/py-xmpppy/files/patch-xmpp-transports.py - информация об исправлении ошибки в модуле)
- https://pypi.python.org/pypi/eonums/0.9.0 - простенький конвертер числительных на Эсперанто в числа и наоборот. На данный момент для ManSPy написан собственный код конвертирования в числа, который понимает части речи, производные от числительных.
- TKinter - может требоваться на ОС Linux (команда для установки: "aptitude install python3-tk")

Для запуска программы служит файл run.py, размещёнеый в корне репозитория. В файле присутствуют словарь, позволяющий включать/отключать модули интерфейсов (МИ), через которые происходит взаимодействие пользователя с программой:
```python
interfaces = {
  'autofeed':    1, # Автоподатчик, включён
  'TKinter':     1, # Примитивный чатб включён
  'jabber':      0, # Jabber,  выключен, но можно включить
  'vkcom':       0, # ВКонтакте, выключен из-за наличия ошибок
  'Commandline': 0  # Один из первых МИ, выключен так как не имеет смысла
  }
```

Есть ещё файл с настройками для авторизации в Jabber и ВКонтакте. Он расположен уровнем выше директории репозитория, имеет имя  IFM_passwords.txt и следующее содержимое в формате JSON:
```json
{
  "jabber": {
    "login": "ИмяПользователя@Сервер",
    "pass": "Пароль"
  },
  "vkcom": {
    "app_id": "ИдентификаторПриложения",
    "login": "ТелефонИлиЭлАдрес",
    "pass": "Пароль"
  }
}
```
Данный файл необходимо создать вручную, если хотите использовать интерфейс Jabber.


# Файлы, генерируемые программой

После запуска появится директория DATA_BASE (расположена уровнем выше директории проекта), в которой будут сгенерированы следующие файлы:
- analysis.txt - результаты анализа предложений (графематический, морфологический, постморфологический, синтаксический). Сюда же пишутся предложения на внутреннем языке (ВЯ), которые строятся на основе анализов и содержат выполняемые программой функции.
- comparing_fasif.txt - результаты сравнения актанта (словосочетания) со словосочетанием в ФАСИФе.
- history.txt - история диалога отдельно для каждого модуля интерфейсов (МИ)

А также директория Esperanto, в которой лежит файл БД main_data.db.

# Директории репозитория

Репозиторий расположен в директории ManSPy (но может быть и любое другое имя), в которой расположены ещё две директории:
- ManSPy - сама программа
- IFModules - модули интерфейсов (МИ), выполненные в виде отдельных маленьких программ. В них реализованы варианты взаимодействия с программой: примитивный чат на TKinter'е, автоподатчик (используется для автоматической поочередной подачи предложений), доступ из чатов Jabber'а. Там же реализован механизм параллельной работы всех запущенных МИ и программы ManSPy. Вы можете писать собственные МИ, например, для доступа к программе из социальных сетей, виртуальных миров, а с использованием распознавания речи можно написать МИ для доступа через сотовую связь, также есть возможный вариант применения интерфейсов мозг-компьютер.

В файле run.py происходит создание объекта программы и его передача в модули интерфейсов. Объект программы имеет следующие функции, которые вызываются МИ:
- write_text(IF, w_text) - принимает МИ и текст на естественном языке.

В свою очередь модуль интерфейса должен содержать следующие функции, которые вызываются ManSPy:
- init() - инициализация модуля
- to_IF(read_text) - передаёт ответ

# ФАСИФ - формат ассоциирования слов и функций.

ФАСИФ - это формат, в котором удобно описывать ассоциации между функцией и глаголом и/или словосочетанием. В ассоциациях лингвистическую информацию можно писать сразу для нескольких языков, хотя пока доступен один - Эсперанто. Существует два вида ФАСИФа.

Первый вид - это ассоциация функции и глагола. В данном случае указывается функция и имя глагола, возможно, с синонимами. В функцию будут передаваться состояния словосочетаний, которые могут быть выведены в качестве ответов, но могут быт и другие варианты использования (зависит от указанной функции). О состоянии словосочетания - ниже. Например доступен для использования глагол montru, выводящий состояния в МИ. Глаголы могут быть переопределены в ФАСИФе второго вида для каждого словосочетания отдельно.

Второй вид - это ассоциация функции и словосочетания, а также функции и глагола, связанного со словосочетанием. В нём подробно описываются аргументы функции, их соответствие словам в конкретном словосочетании. Слово, ассоциированное с аргументом функции, называется аргументным. Причём для аргументного слова указываются гиперонимы - абстрактные группы, в которые это аргументное слово может входить. Кроме этого, для аргументов, при необходимости, указывается таблица конвертации, в которой указываются возможные аргументные слова и то, на что они должны замениться перед передачей в функцию, если не указано, то в функцию передаётся корень слова.

Каждое словосочетание может иметь несколько глаголов, и для каждого - своя функция.

В данный момент реализованы ФАСИФы для получения курса валют, включения/выключения света - сейчас сделана эмуляция, получения IP-адреса компьютера.

# Как работает ManSPy

Над предложением, поступающем от пользователя, производятся лингвистические анализы. Затем, происходит выбор соответствующих ФАСИФов для актантов глагола (словосочетаний), после чего анализы на основе ФАСИФа конвертируются во внутренний язык. Предложение на внутреннем языке интерпретируется модулем выполнения функций (МВФ).

# Написание собственных МИ

Модули МИ находятся в /IFModules и имеет имя IFM_*.py, где * (звёздочка) - имя Вашего модуля. Модуль содержит класс с именем Interface. Класс имеет слеующую структуру:

```python

class Interface():
    def __init__(self, API):
        self.API = API
        self.settings = {} # настройки ManSPy, действующие только для данного МИ. Необязательны.

    def your_name(self):
        ''' Одна из Ваших любых функций с любым именем и любыми аргументами. '''

        # передаём сообщение в ManSPy. Ответ от ManSPy будет передан в self.read_text.
        # any_data - необязательный аргумент. Будет передан в self.read_text.
        self.API.write_text(self, "Ваше сообщение", any_data)

    def read_text(self, r_text, any_data):
        ''' Функция принимает: r_text - ответ от Manspy, any_data - произвольная информация от данного класса 
        '''

    def init(self):
        ''' код инициализации модуля '''


```

# Подробно о ФАСИФе