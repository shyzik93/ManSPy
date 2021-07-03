import json


class FasifDB:
    fasifs = {}

    def __init__(self, c, cu):
        pass

    def safe(self, type_fasif, fasif):
        fasifs = self.fasifs.setdefault(type_fasif, [])
        fasifs.append(fasif)

    def get(self, type_fasif):
        return self.fasifs.get(type_fasif, [])


class FasifDB_old:
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
