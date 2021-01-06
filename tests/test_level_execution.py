""" TODO:
В примерах должна присутствовать такая последловательность:
1. Пробуем обратитьс по несуществующему синониму (или обратиться к факту. Ответ будет о не знании синонима (факта)
2. Вводим предложение, которые заносит данные в базу (факты, синонимы и так далее).
3. Пробуем вести предложение из шага 1 повторно. Ответ должен быть дан, т. к. программа теперь знает синониме (факте).
"""

import unittest

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
    dataset_undirect_order_of_words
)


class LevelRTextTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = Settings(answer_type='construct', history=False)
        cls.api = API().__enter__()

    def setUp(self):
        self.answers = {}
        self.answers_true = {}
        self.settings.read_text = self.read_text

    def check_answers(self):
        for input_data, output_data in self.answers.items():
            self.assertListEqual(
                self.answers[input_data],
                self.answers_true[input_data][0],
                self.answers_true[input_data][1]
            )

    @classmethod
    def tearDownClass(cls):
        cls.api.__exit__(None, None, None)

    def read_text(self, r_text, any_data):
        input_data = any_data
        self.answers[input_data].append(r_text)

    def pass_example_to_manspy(self, example):
        self.settings.language = example.get('language', 'esperanto')
        input_data = example['w_text']
        true_answer = example['r_text_construct']
        self.answers.setdefault(input_data, [])
        self.answers_true.setdefault(input_data, [true_answer, input_data])
        self.api.write_text(input_data, self.settings, {'any_data': input_data, 'print_time': False})

    def test_verb_and_actants(self):
        for example in dataset_verb_and_actants['examples']:
            self.pass_example_to_manspy(example)

        self.check_answers()

    def test_verb_and_repeated_actants(self):
        for example in dataset_verb_and_repeated_actants['examples']:
            self.pass_example_to_manspy(example)

        self.check_answers()

    def test_verb_and_homogeneous_actants(self):
        for example in dataset_verb_and_homogeneous_actants['examples']:
            self.pass_example_to_manspy(example)

        self.check_answers()

    def test_antonym_of_verb(self):
        for example in dataset_antonym_of_verb['examples']:
            self.pass_example_to_manspy(example)

        self.check_answers()

    def test_verb_and_homogeneous_direct_supplement(self):
        for example in dataset_verb_and_homogeneous_direct_supplement['examples']:
            self.pass_example_to_manspy(example)

        self.check_answers()

    def test_punctuation(self):
        for example in dataset_punctuation['examples']:
            self.pass_example_to_manspy(example)

        self.check_answers()

    def test_numbers_and_simple_math(self):
        for example in dataset_numbers_and_simple_math['examples']:
            self.pass_example_to_manspy(example)

        self.check_answers()

    def test_synonyms_of_verb(self):
        for example in dataset_synonyms_of_verb['examples']:
            self.pass_example_to_manspy(example)

        self.check_answers()

    def test_undirect_order_of_words(self):
        for example in dataset_undirect_order_of_words['examples']:
            self.pass_example_to_manspy(example)

        self.check_answers()