import unittest

from analyzers import esperanto_graphemathic
from manspy import unit


@unittest.skip
class TestGraphemathicalAnalysis(unittest.TestCase):
    def test_define_type_symbol(self):
        word = unit.Word('montru')
        word(0, 'type', 'letter')
        word(1, 'type', 'letter')
        word(2, 'type', 'letter')
        word(3, 'type', 'letter')
        word(4, 'type', 'letter')
        word(5, 'type', 'letter')

        word_result = unit.Word('montru')
        result = esperanto_graphemathic.define_type_symbol(word_result)

        message = 'define_type_symbol: "{}" must be "{}", not "{}"'

        for symbol_index, symbol in word:
            type_ethalon = word(symbol_index, 'type')
            type_result = word_result(symbol_index, 'type')
            self.assertEqual(
                type_ethalon,
                type_result,
                message.format(symbol, type_ethalon, type_result)
            )
            #print(symbol, type_ethalon, type_result)
    
    def _test_process_end_of_word(self, source, word, end, end_orig):
        message = 'word:{} end:{} end_orig:{}'

        word_ethalon = unit.Word(source)
        word_ethalon['word'] = word
        word_ethalon['end'] = end
        word_ethalon['end_orig'] = end_orig

        word_result = unit.Word(source)
        esperanto_graphemathic.process_end_of_word(word_result)
        self.assertEqual(
            message.format(word_ethalon['word'], word_ethalon['end'], word_ethalon['end_orig']),
            message.format(word_result['word'], word_result['end'], word_result['end_orig']),
            source
        )

    def test_process_end_of_word(self):
        self._test_process_end_of_word('montru', 'montru', '', '')
        self._test_process_end_of_word('kurso.', 'kurso', '.', '.')
        self._test_process_end_of_word('kurso?!!', 'kurso', '?', '?!!')
        self._test_process_end_of_word('kurso...', 'kurso', '...', '...')
        self._test_process_end_of_word('kurso..', 'kurso', '...', '..')
        self._test_process_end_of_word('kurso......', 'kurso', '...', '......')
        self._test_process_end_of_word('kurso,', 'kurso', ',', ',')
        self._test_process_end_of_word('kurso,,', 'kurso', ',', ',,')
        self._test_process_end_of_word('kurso:', 'kurso', ':', ':')

    def test_process_words(self):
        source_string = 'montru'
        text_ethalon = [unit.Word('montru')]
        text_ethalon[0]['end'] = ''
        text_ethalon[0]['end_orig'] = ''
        text_result = esperanto_graphemathic.process_words(source_string)
        self.assertEqual(len(text_result), len(text_ethalon), source_string)
        self.assertEqual(text_ethalon[0].unit_info, text_result[0].unit_info, source_string)

        source_string = 'montru ,, sxaltu'
        text_ethalon = [unit.Word('montru'), unit.Word('ŝaltu')]
        text_ethalon[0]['word'] = 'montru'
        text_ethalon[0]['end'] = ','
        text_ethalon[0]['end_orig'] = ',,'
        text_ethalon[1]['word'] = 'ŝaltu'
        text_ethalon[1]['end'] = ''
        text_ethalon[1]['end_orig'] = ''
        text_result = esperanto_graphemathic.process_words(source_string)
        self.assertEqual(len(text_result), len(text_ethalon), source_string)
        for word_ethalon, word_result in zip(text_result, text_ethalon):
            self.assertEqual(word_ethalon.unit_info, word_result.unit_info, source_string)
        for word in text_result:
            print(word['word']+word['end'], end=' ')
        print()

        source_string = 'montru  "kurson"?!!!'
        text_ethalon = [unit.Word('montru'), unit.Word('"kurson"?!!!')]
        text_ethalon[0]['word'] = 'montru'
        text_ethalon[0]['end'] = ''
        text_ethalon[0]['end_orig'] = ''
        text_ethalon[1]['word'] = 'kurson'
        text_ethalon[1]['end'] = '?'
        text_ethalon[1]['end_orig'] = '?!!!'
        text_ethalon[1]['around_pmark'] = ['quota']
        text_result = esperanto_graphemathic.process_words(source_string)
        self.assertEqual(len(text_result), len(text_ethalon), source_string)
        for word_ethalon, word_result in zip(text_result, text_ethalon):
            self.assertEqual(word_ethalon.unit_info, word_result.unit_info, source_string)
        for word in text_result:
            print(word['word']+word['end'], end=' ')
        print()


if __name__ == '__main__':
    unittest.main()