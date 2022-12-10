from typing import Optional, Union

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
    dct_speeches = {'noun': 1, 'verb': 2, 'adjective': 3, 'adverb': 4}

    def __init__(self, database_settings):
        self.fasif = FasifDB()
        self.max_group_index = 0
        self.max_word_id = 0
        self.word_by_id = {}
        self.id_by_word = {}

    def close(self):
        pass

    def get_fasif(self, type_fasif):
        return self.fasif.get(type_fasif)

    def save_fasif(self, type_fasif, fasif):
        self.fasif.safe(type_fasif, fasif)

    def _speech2id(self, speech: Optional[Union[str, int]]) -> int:
        return self.dct_speeches[speech] if isinstance(speech, str) else speech

    def get_new_index(self):
        self.max_group_index += 1
        return self.max_group_index

    # Работа с таблицей words

    def add_word(self, *words: str) -> int:
        for word in words:
            self.max_word_id += 1
            word = word.lower()
            self.word_by_id[self.max_word_id] = word
            self.id_by_word[word] = self.max_word_id

        return self.max_word_id

    def word2id(self, word: str) -> int:
        if isinstance(word, int):
            return word

        word_id = self.id_by_word.get(word)
        return word_id if word_id else self.add_word(word)

    def convert(self, *inlist):
        ''' Преобразовывает id в слово или слово в id '''
        for el in inlist:
            if isinstance(el, int):
                word = self.word_by_id.get(el)
                if not word:
                    raise Exception(f'Word with id {el} not found')
                yield word
            else:
                word_id = self.id_by_word.get(el)
                yield word_id if word_id else self.add_word(el)

    # Работа с таблицей relations