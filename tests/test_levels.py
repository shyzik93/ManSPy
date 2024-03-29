""" TODO:
В примерах должна присутствовать такая последловательность:
1. Пробуем обратитьс по несуществующему синониму (или обратиться к факту. Ответ будет о не знании синонима (факта)
2. Вводим предложение, которые заносит данные в базу (факты, синонимы и так далее).
3. Пробуем вести предложение из шага 1 повторно. Ответ должен быть дан, т. к. программа теперь знает синониме (факте).
"""
import unittest
from unittest.mock import patch

from manspy.utils.settings import Settings, InitSettings
from tests.datasets_of_analyzes import datasets
from manspy.runners.simple import runner


def mock_action(path):
    return path


def sort_text_dict(text):
    for sentence_index, sentence in text['subunits'].items():
        for word_index, word in sentence['subunits'].items():
            unit_info = {}
            for k in sorted(word['unit_info'].keys()):
                unit_info[k] = word['unit_info'][k]

            word['unit_info'] = unit_info


class LevelsTestCase(unittest.TestCase):
    def test_level_morphological(self):
        settings = Settings(answer_type='construct', history=False)
        with InitSettings():
            for dataset in datasets:
                for example in dataset['examples']:
                    if not example.get('morphological'):
                        continue

                    with self.subTest(dataset['description']):
                        settings.language = example.get('language', 'esperanto')
                        answers = runner(example['w_text'], settings, pipeline=':morph')
                        #sort_text_dict(example['morphological'])
                        answer = answers.export_unit(dict)
                        #sort_text_dict(answer)
                        self.assertDictEqual(answer, example['morphological'], example['w_text'])

    @patch('manspy.analyzers.converter_internal_sentences.importer')
    def test_level_convert(self, importer):
        importer.import_action = mock_action

        settings = Settings(answer_type='construct', history=False)
        with InitSettings():
            for dataset in datasets:
                for example in dataset['examples']:
                    if not example.get('convert'):
                        continue

                    with self.subTest(dataset['description']):
                        settings.language = example.get('language', 'esperanto')
                        answers = runner(example['w_text'], settings, pipeline=':convert')
                        self.assertDictEqual(answers, example['convert'], example['w_text'])

    def test_level_execution(self):
        settings = Settings(answer_type='construct', history=False)
        with InitSettings():
            for dataset in datasets:
                for example in dataset['examples']:
                    if not example.get('r_text_construct'):
                        continue

                    with self.subTest(dataset['description']):
                        settings.language = example.get('language', 'esperanto')
                        answers = runner(example['w_text'], settings)
                        answers = [answer for answer in answers]
                        self.assertListEqual(answers, example['r_text_construct'], example['w_text'])
