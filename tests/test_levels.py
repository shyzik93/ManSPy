""" TODO:
В примерах должна присутствовать такая последловательность:
1. Пробуем обратитьс по несуществующему синониму (или обратиться к факту. Ответ будет о не знании синонима (факта)
2. Вводим предложение, которые заносит данные в базу (факты, синонимы и так далее).
3. Пробуем вести предложение из шага 1 повторно. Ответ должен быть дан, т. к. программа теперь знает синониме (факте).
"""
import os
import unittest
from unittest.mock import patch, Mock

from manspy import API, Settings
from tests.datasets_of_analyzes import datasets


DEFAULT_MODULE_DIR = os.path.dirname(__file__)
LEN_DEFAULT_MODULE_DIR = len(DEFAULT_MODULE_DIR) + 2


def mock_action(path):
    return path[LEN_DEFAULT_MODULE_DIR:]


class LevelsTestCase(unittest.TestCase):
    @patch('manspy.converter.importer')
    def test_level_convert(self, importer):
        def send_to_out(r_text, _):
            pass

        importer.action = mock_action

        settings = Settings(
            answer_type='construct',
            history=False,
            send_to_out=send_to_out,
            levels='graphmath:convert'
        )
        with API() as api:
            for dataset in datasets:
                for example in dataset['examples']:
                    with self.subTest(dataset['description']):
                        settings.language = example.get('language', 'esperanto')
                        msg, answers = api.send_to_in(example['w_text'], settings)
                        self.assertDictEqual(answers, example['convert'], example['w_text'])

    def test_level_execution(self):
        def send_to_out(r_text, _):
            answers.append(r_text)

        answers = []
        settings = Settings(answer_type='construct', history=False, send_to_out=send_to_out)
        with API() as api:
            for dataset in datasets:
                for example in dataset['examples']:
                    with self.subTest(dataset['description']):
                        answers.clear()
                        settings.language = example.get('language', 'esperanto')
                        api.send_to_in(example['w_text'], settings)
                        self.assertListEqual(answers, example['r_text_construct'], example['w_text'])
