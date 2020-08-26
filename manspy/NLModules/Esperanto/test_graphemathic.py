import unittest

from manspy.NLModules.Esperanto import GraphemathicAnalysis
from manspy.NLModules import ObjUnit


class TestGraphemathicalAnalysis(unittest.TestCase):
    def test_define_type_symbol(self):
        word = ObjUnit.Word('montru')
        word(0, 'type', 'letter')
        word(1, 'type', 'letter')
        word(2, 'type', 'letter')
        word(3, 'type', 'letter')
        word(4, 'type', 'letter')
        word(5, 'type', 'letter')

        word_result = ObjUnit.Word('montru')
        result = GraphemathicAnalysis.define_type_symbol(word_result)

        message = 'define_type_symbol: "{}" must be "{}", not "{}"'

        for symbol_index, symbol in word:
            type_ethalon = word(symbol_index, 'type')
            type_result = word_result(symbol_index, 'type')
            self.assertEqual(
                type_ethalon,
                type_result,
                message.format(symbol, type_ethalon, type_result)
            )
            print(symbol, type_ethalon, type_result)


if __name__ == '__main__':
    unittest.main()