def get_sqlite3(db_settings):
    import sqlite3
    sqlite3.enable_callback_tracebacks(True)
    c = sqlite3.connect(db_settings['path'])
    c.row_factory = sqlite3.Row
    return c, c.cursor()


def get_mysql(db_settings):
    c = None
    cu = None
    return c, cu


def get_postgresql(db_settings):
    c = None
    cu = None
    return c, cu