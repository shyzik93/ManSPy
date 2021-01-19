import os
import unittest
from unittest.mock import patch

from manspy import API, Settings
from tests.datasets_of_analyzes import datasets


DEFAULT_MODULE_DIR = os.path.dirname(__file__)
LEN_DEFAULT_MODULE_DIR = len(DEFAULT_MODULE_DIR) + 2


def mock_action(path):
    return path[LEN_DEFAULT_MODULE_DIR:]


@patch('manspy.converter.importer.action', mock_action)
class LevelRTextTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = API().__enter__()

    def setUp(self):
        self.settings = Settings(
            answer_type='construct',
            history=False,
            send_to_out=self.send_to_out,
            levels='graphmath:convert'
        )

    @classmethod
    def tearDownClass(cls):
        cls.api.__exit__(None, None, None)

    def send_to_out(self, r_text, any_data):
        pass

    def test_level_convert(self):
        for dataset in datasets:
            for example in dataset['examples']:
                with self.subTest(dataset['description']):
                    self.settings.language = example.get('language', 'esperanto')
                    msg, answers = self.api.send_to_in(example['w_text'], self.settings)
                    self.assertDictEqual(answers, example['convert'], example['w_text'])
