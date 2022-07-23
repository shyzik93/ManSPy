import json
import sqlite3


class FasifDB:
    def __init__(self, c, cu):
        self.c, self.cu = c, cu
        self.cu.execute('''
            CREATE TABLE IF NOT EXISTS fasifs (
                id_fasif INTEGER PRIMARY KEY AUTOINCREMENT,
                type_fasif TEXT,
                fasif TEXT UNIQUE ON CONFLICT IGNORE
        );''')

    def safe(self, type_fasif, fasif):
        self.cu.execute(
            'INSERT INTO fasifs (type_fasif, fasif) VALUES (?,?)',
            (type_fasif, json.dumps(fasif, sort_keys=True))
        )
        self.c.commit()

    def get(self, type_fasif):
        rows = self.cu.execute('SELECT fasif FROM fasifs WHERE type_fasif=?', (type_fasif,))
        for row in rows:
            yield json.loads(row['fasif'])


class Database:
    def __init__(self, database_settings):
        sqlite3.enable_callback_tracebacks(True)
        self.c = sqlite3.connect(database_settings['path'])
        self.c.row_factory = sqlite3.Row
        self.cu = self.c.cursor()
        self.fasif = FasifDB(self.c, self.cu)

    def get_fasif(self, type_fasif):
        return self.fasif.get(type_fasif)

    def save_fasif(self, type_fasif, fasif):
        self.fasif.safe(type_fasif, fasif)
