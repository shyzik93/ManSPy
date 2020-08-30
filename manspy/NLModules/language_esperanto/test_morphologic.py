import unittest

from manspy.NLModules.Esperanto import MorphologicalAnalysis
from manspy.NLModules import ObjUnit

class TestMorphologicalAnalysis(unittest.TestCase):
    def test_is_numeric(self):
        numbers = {
            0: ['nul'],
            1: ['unu'],
            2: ['du'],
            # TODO: распознавание 'dektri' как 'dek tri'
            #13: ['dektri'], # Правильно писать: 'dek tri'
            40: ['kvardek'],
            50: ['kvindek'],
        }
        
        for numeric, alphabetics in numbers.items():
            for alphabetic in alphabetics:
                word = ObjUnit.Word(alphabetic)
                is_numeric = MorphologicalAnalysis.is_numeral(word['word'], word)
                print(is_numeric, alphabetic, numeric, word['number_value'])

if __name__ == '__main__':
    unittest.main()