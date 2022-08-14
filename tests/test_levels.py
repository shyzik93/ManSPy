""" TODO:
В примерах должна присутствовать такая последловательность:
1. Пробуем обратитьс по несуществующему синониму (или обратиться к факту. Ответ будет о не знании синонима (факта)
2. Вводим предложение, которые заносит данные в базу (факты, синонимы и так далее).
3. Пробуем вести предложение из шага 1 повторно. Ответ должен быть дан, т. к. программа теперь знает синониме (факте).
"""
import os
import unittest
from unittest.mock import patch

from manspy.analyse_text import nature2internal
from manspy.message import Message
from manspy.utils.settings import Settings, InitSettings
from tests.datasets_of_analyzes import datasets


DEFAULT_MODULE_DIR = os.path.dirname(__file__)
LEN_DEFAULT_MODULE_DIR = len(DEFAULT_MODULE_DIR) + 2


def mock_action(path):
    return path[LEN_DEFAULT_MODULE_DIR:]


def sort_text_dict(text):
    for sentence_index, sentence in text['unit'].items():
        for word_index, word in sentence['unit'].items():
            unit_info = {}
            for k in sorted(word['unit_info'].keys()):
                unit_info[k] = word['unit_info'][k]

            word['unit_info'] = unit_info


class LevelsTestCase(unittest.TestCase):
    def test_level_morphological(self):
        settings = Settings(
            answer_type='construct',
            history=False,
            levels='graphmath:morph'
        )
        with InitSettings():
            for dataset in datasets:
                for example in dataset['examples']:
                    if not example.get('morphological'):
                        continue

                    with self.subTest(dataset['description']):
                        settings.language = example.get('language', 'esperanto')
                        answers = nature2internal(Message(settings, example['w_text']))
                        #sort_text_dict(example['morphological'])
                        answer = answers.export_unit(dict)
                        #sort_text_dict(answer)
                        self.assertDictEqual(answer, example['morphological'], example['w_text'])

    @patch('manspy.converter.importer')
    def test_level_convert(self, importer):
        importer.import_action = mock_action

        settings = Settings(
            answer_type='construct',
            history=False,
            levels='graphmath:convert'
        )
        with InitSettings():
            for dataset in datasets:
                for example in dataset['examples']:
                    if not example.get('convert'):
                        continue

                    with self.subTest(dataset['description']):
                        settings.language = example.get('language', 'esperanto')
                        answers = nature2internal(Message(settings, example['w_text']))
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
                        answers = nature2internal(Message(settings, example['w_text']))
                        answers = [answer for answer in answers]
                        self.assertListEqual(answers, example['r_text_construct'], example['w_text'])
