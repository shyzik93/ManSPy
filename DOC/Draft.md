



# Изменение состояние словосочетания: sxaltu tablan lampon en cxambro
Функция ассоциирована с комбинацией глагола и словосочетаний
1. "sxaltu-lampon"("tablan", "cxambro")

# Получение состояния словосочетания: montru dolaran kurson
Функция ассоциирована с глаголом. Дополнительные функции ассоциированы со словосочетанием

Выполняются поочерёдно:
1. variable1 = some_function("dolaran", "kurson") # получение состояния актанта
2. "montru"(variable1)

В виде внутреннего языка:
```python
{'circumstance': []  # обстоятельства,
'functions': [{
    'fasif_type': 'word_combination',   # актант глагола (словосочетание)
    'sub_type': 'get_condition',  # получить состояние актанта. Другие варианты: set_condition
    'function': get_cource,
    'arguments': [
        {'value': 'USD', 'is_negative': False},
        {'value': 'Russia', 'is_negative': False}
    ],
    'verb_function': print   # функция из шага 2. В неё функция get_cource может отправлять ответы в другом потоке согласно обстоятельству времени (например, каждые 2 часа, через 1 час или в 14:30)
}, {
    'fasif_type': VERB,
    'sub_type': None,  # у типа "verb" не быват подтипов
    'function': print,
    'arguments': [РезультатШага1ЕслиЕсть],
    'is_antonim': False
}]
}
```
Выполняется с начала до конца. При этом,


4. покажи АКТАНТ!, АКТАНТ2 и АКТАНТ3
измени ИЗМЕНЯЕМЫЙ-АКТАНТ на НОВОЕ-ЗНАЧЕНИЕ : глагол, устанавливающий новое значение
включи/ ИЗМЕНЯЕМЫЙ-АКТАНТ  


5. Если курс доллара больше 10, то покажи 5 и включи свет, иначе покажи 50.
```
   Перед выполнением:   IdentLevel=0 ExecLevel=True
   1. IdentLevel=0 ExecLevel=True  (условие истинно)            Если курс доллара больше 10
   2. IdentLevel=1 ExecLevel=True                               покажи 5
   3. IdentLevel=1 ExecLevel=True                               включи свет
   4. IdentLevel=0 ExecLevel=False (при иначе - инвертируем)    Иначе
   5. IdentLevel=1 ExecLevel=False                              иначе покажи 50
```