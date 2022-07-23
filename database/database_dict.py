class FasifDB:
    fasifs = {}

    def __init__(self):
        pass

    def safe(self, type_fasif, fasif):
        fasifs = self.fasifs.setdefault(type_fasif, [])
        fasifs.append(fasif)

    def get(self, type_fasif):
        return self.fasifs.get(type_fasif, [])


class Database:
    def __init__(self, database_settings):
        self.fasif = FasifDB()

    def get_fasif(self, type_fasif):
        return self.fasif.get(type_fasif)

    def save_fasif(self, type_fasif, fasif):
        self.fasif.safe(type_fasif, fasif)
