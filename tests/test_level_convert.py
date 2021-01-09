import os
import unittest
from unittest.mock import patch

from manspy import API, Settings
from tests.datasets_of_analyzes import (
    dataset_verb_and_actants,
    dataset_verb_and_repeated_actants,
    dataset_verb_and_homogeneous_actants,
    dataset_antonym_of_verb,
    dataset_verb_and_homogeneous_direct_supplement,
    dataset_punctuation,
    dataset_numbers_and_simple_math,
    dataset_synonyms_of_verb,
    dataset_undirect_order_of_words,
    dataset_mistakes
)


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
        self.settings = Settings(answer_type='construct', history=False, read_text=self.read_text)

    @classmethod
    def tearDownClass(cls):
        cls.api.__exit__(None, None, None)

    def read_text(self, r_text, any_data):
        pass

    def pass_example_to_manspy(self, example):
        self.settings.language = example.get('language', 'esperanto')
        input_data = example['w_text']
        true_answer = example['convert']
        msg, answers = self.api.write_text(input_data, self.settings, {'print_time': False, 'levels': 'graphmath:convert'})
        self.assertDictEqual(answers, true_answer, input_data)

    def test_verb_and_actants(self):
        for example in dataset_verb_and_actants['examples']:
            self.pass_example_to_manspy(example)

    def test_verb_and_repeated_actants(self):
        for example in dataset_verb_and_repeated_actants['examples']:
            self.pass_example_to_manspy(example)

    def test_verb_and_homogeneous_actants(self):
        for example in dataset_verb_and_homogeneous_actants['examples']:
            self.pass_example_to_manspy(example)

    def test_antonym_of_verb(self):
        for example in dataset_antonym_of_verb['examples']:
            self.pass_example_to_manspy(example)

    def test_verb_and_homogeneous_direct_supplement(self):
        for example in dataset_verb_and_homogeneous_direct_supplement['examples']:
            self.pass_example_to_manspy(example)

    def test_punctuation(self):
        for example in dataset_punctuation['examples']:
            self.pass_example_to_manspy(example)

    def test_numbers_and_simple_math(self):
        for example in dataset_numbers_and_simple_math['examples']:
            self.pass_example_to_manspy(example)

    def test_synonyms_of_verb(self):
        for example in dataset_synonyms_of_verb['examples']:
            self.pass_example_to_manspy(example)

    def test_undirect_order_of_words(self):
        for example in dataset_undirect_order_of_words['examples']:
            self.pass_example_to_manspy(example)

    def test_mistakes(self):
        for example in dataset_mistakes['examples']:
            self.pass_example_to_manspy(example)
