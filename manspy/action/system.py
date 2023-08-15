settings = None


def add_group(arg0, group=0, word=0):
    print("Group is added:", group, "in", word)
    print("Getted settings:", settings)
    yield 'test add'


def get_group(arg0, group=0, word=0):
    print("Group is got:", word, "in", group)
    print("got settings:", settings)
    yield 'test get'
