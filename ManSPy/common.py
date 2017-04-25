# -*- coding: utf-8 -*-
import os, sqlite3 as sql

sql.enable_callback_tracebacks(True)

def create_bd_file(language, name):
    if not os.path.exists(language) or not os.path.isdir(language):
        os.mkdir(language)
    name = os.path.join(language, name)
    c = sql.connect(name)
    c.row_factory = sql.Row
    cu = c.cursor()
    return c, cu