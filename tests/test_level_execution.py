""" TODO:
В примерах должна присутствовать такая последловательность:
1. Пробуем обратитьс по несуществующему синониму (или обратиться к факту. Ответ будет о не знании синонима (факта)
2. Вводим предложение, которые заносит данные в базу (факты, синонимы и так далее).
3. Пробуем вести предложение из шага 1 повторно. Ответ должен быть дан, т. к. программа теперь знает синониме (факте).
"""
from unittest import TestCase

from manspy import API, Settings
from tests.datasets_of_analyzes import datasets


class LevelRTextTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = API().__enter__()

    def setUp(self):
        self.settings = Settings(answer_type='construct', history=False, send_to_out=self.send_to_out)
        self.answers = []

    @classmethod
    def tearDownClass(cls):
        cls.api.__exit__(None, None, None)

    def send_to_out(self, r_text, _):
        self.answers.append(r_text)

    def test_level_execution(self):
        for dataset in datasets:
            for example in dataset['examples']:
                with self.subTest(dataset['description']):
                    self.answers.clear()
                    self.settings.language = example.get('language', 'esperanto')
                    self.api.send_to_in(example['w_text'], self.settings)
                    self.assertListEqual(self.answers, example['r_text_construct'], example['w_text'])
