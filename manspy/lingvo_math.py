''' Модуль математической лингвистии '''
import itertools


def _dproduct(resl, values, key):
    n = len(values)
    _resl = list(resl)
    for i, el in enumerate(resl, 0):
        #_resl.insert(0, [])
        for j in range(n-1):
            _resl.insert(i*n, dict(el))
        #print _resl
        for j in range(n):
            _resl[j+n*i][key] = values[j]#.append(addl[j])
        #print _resl
    #print len(_resl), _resl, '\n'
    return _resl


def dproduct(dparentl):
    ''' Выполняет декартово (прямое) произведение над словарями в списке dparent1
        {'a': [1,2], 'b': [5,6]} -> [{'a': 1, 'b':5}, {'a': 1, 'b':6}, {'a': 2, 'b':5}, {'a': 2, 'b':6}]
        В стандартной библиотеке Python я этой функции не нашёл.
        Функция необходима для аргументных слов.
        [
            (('a',1), ('b',5)),
            (('a',1), ('b',6)),
            (('a',2), ('b',5)),
            (('a',2), ('b',6))
        ]
    '''
    prevchildl = [{}]
    for key, values in dparentl.items():
        prevchildl = _dproduct(prevchildl, values, key)
    return prevchildl

def dproduct2(dparent1):
    l = [([k], v) for k, v in dparent1.items()]
    l = [[i for i in itertools.product(*subl)] for subl in l]
    l = [i for i in itertools.product(*l)]
    l = [dict(i) for i in l]
    return l

if __name__ == '__main__':
    dparentl = {'a': [1, 2, 3, 4],
         'b': [10, 20, 30, 40],
         'c': [100, 200, 300, 400]}

    #dparentl = {'a': [1,2], 'b': [5,6]}

    resl = dproduct(dparentl)
    print(len(resl), resl)

    resl = dproduct2(dparentl)
    print(len(resl), resl)
