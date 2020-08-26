import unittest

import GraphemathicalAnalysis

def t(a):
    return 3

class TestGraphemathicalAnalysis(unittest.TestCase):
    def test_list_int(self):
        #data = {'symbol'}
        #result = GraphemathicalAnalysis.define_type_symbol(data)
        result = t(4)
        self.assertEqual(result, 3)

    def test_list_int2(self):
        #data = {'symbol'}
        #result = GraphemathicalAnalysis.define_type_symbol(data)
        result = t(4)
        self.assertEqual(result, 99)


if __name__ == '__main__':
    unittest.main()