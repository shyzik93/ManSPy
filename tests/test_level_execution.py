""" TODO:
В примерах должна присутствовать такая последловательность:
1. Пробуем обратитьс по несуществующему синониму (или обратиться к факту. Ответ будет о не знании синонима (факта)
2. Вводим предложение, которые заносит данные в базу (факты, синонимы и так далее).
3. Пробуем вести предложение из шага 1 повторно. Ответ должен быть дан, т. к. программа теперь знает синониме (факте).
"""

import unittest

from manspy import API, Settings
from tests.datasets_of_analyzes import datasets

TEST_INPUT_DATAS = {
    'esperanto': datasets
}


class ManSPyTestCase(unittest.TestCase):
    def test_manspy(self):
        def read_text(r_text, any_data):
            input_data, language = any_data
            answers[language][input_data].append(r_text)

        answers = {}
        answers_true = {}

        with API() as api:
            for language, datasets in TEST_INPUT_DATAS.items():
                settings = Settings(read_text=read_text, language=language, answer_type='construct')
                answers.setdefault(language, {})
                answers_true.setdefault(language, {})
                for dataset in datasets:
                    for example in dataset['examples']:
                        input_data = example['w_text']
                        true_answer = example['r_text_construct']
                        if input_data not in answers:
                            answers[language][input_data] = []
                        if input_data not in answers_true:
                            answers_true[language][input_data] = [true_answer, input_data]
                        api.write_text(input_data, settings, {'any_data': [input_data, language], 'print_time': False})

            for language, _answers in answers.items():
                for input_data, output_data in _answers.items():
                    self.assertListEqual(
                        answers[language][input_data],
                        answers_true[language][input_data][0],
                        answers_true[language][input_data][1]
                    )


if __name__ == '__main__':
    test_manspy = TestManSPy()
    test_manspy.test_manspy()
