TEST_INPUT_DATA_ESPERANTO = [
    ('montru dolaran kaj euxran kurzon de rusia banko', ['USD-Russia', 'EUR-Russia']),
    ('sxaltu tablan lampon en dormcxambro', ['1']),
    ('montru adreson de komputilo', ['192.168.0.1']),
    ('montru adreson de androido', []),

    ('dolaran kurzon montru', ['USD-Russia']),
    ('montru de rusia banko euxran kurzon', ['EUR-Russia']),

    # Повторяющиеся аргументы (однородные слова)
    ('montru dolaran kaj dolaran kurzon de rusia banko', ['USD-Russia', 'USD-Russia']),
    ('montru dolaran kaj dolaran kurzon de rusia kaj rusia banko', [
        'USD-Russia',
        'USD-Russia',
        'USD-Russia',
        'USD-Russia'
    ]),
    # Это предложение выдаёт курс доллара только по росбанку (украинский не замечает).
    # TODO: Как вариант решения: проверять каждоый однородный член у дополнений (кроме первого)
    #  (однородные члены должны совпадать по части речи)
    #('montru dolaran kurzon de rusia banko kaj ukraina banko', ['USD-Russia', 'USD-Ukrain']),
    ('montru adreson de komputilo kaj androido', ['192.168.0.1']),
    # Много аргументов (сложатся друг с другом поочерёдно - декартово произведение)
    ('montru euxran kaj dolaran kurzon de ukrainia kaj rusia kaj belarusia banko', [
        'EUR-Russia',
        'EUR-Belarus',
        'EUR-Ukraine',
        'USD-Russia',
        'USD-Belarus',
        'USD-Ukraine',
    ]),
    ('montru euxran kaj dolaran kurzon de ukrainia kaj rusia banko', [
        'EUR-Russia',
        'EUR-Ukraine',
        'USD-Russia',
        'USD-Ukraine'
    ]),
    # TODO: сложатся соответственно (не реализовано пока)
    # ('montru euxran kaj dolaran kurzon de ukrainia kaj rusia banko соответсвенно', [
    #     'EUR-Russia',
    #     'EUR-Ukraine',
    #     'USD-Russia',
    #     'USD-Ukraine'
    # ]),
    # TODO: однородные слова-посредники (не реализовано пока)
    #('montru dolaran kurzon de ukrainia banko kaj de rusia banko', ['USD-Ukraine', 'USD-Russia']),
    # антонимия. Можно через приставку, которая антонимирует значение, а можно через глагол-антоним
    ('malsxaltu tablan lampon en dormcxambro kaj fermo', ['0']),
    ('malmontru dolaran kurzon de rusia banko de mia domo', []),
    # однородные прямые дополнения, по сути - две разных функции (два разных действия) в одном предложении.
    ('montru adreson de komputilo kaj dolaran kurzon', ['192.168.0.1', 'USD-Russia']),
    ('montru adreson de komputilo kaj dolaran kurzon de belarusia banko', ['192.168.0.1', 'USD-Belarus']),
    ('montru dolaran kurzon kaj adreson de komputilo', ['USD-Russia', '192.168.0.1']),
    # Пунктуация
    ('montru euxran, dolaran kurzon de ukrainia banko.', ['EUR-Ukraine', 'USD-Ukraine']),
    ('montru euxran, dolaran kurzon de ukrainia banko .', ['EUR-Ukraine', 'USD-Ukraine']),
    ('montru euxran, dolaran kurzon de ukrainia banko ...', ['EUR-Ukraine', 'USD-Ukraine']),
    # ('Montru dolaran kurzon. Montru euxran kurzon de belarusia banko', []),
    # TODO: пока не поддерживаются
    # ('montru dolaran kurzon, kiu estas dolara', []),
    # ('Se euxra cambio de belarusia banko estas sepduk kvar, do sxaltu tablan lampon en dormcxambro', []),
    # ('Do sxaltu tablan lampon en dormcxambro, se euxra cambio de belarusia banko estas sepduk kvar', []),
    ('adiciu dudekon trion', ['23']),
    ('adiciu kvardekon kaj trion kaj milionon', ['40 + 3 + 1000000']),
    ('maladiciu dolaran kurzon kaj trion', ['3']),  # TODO correct: ['USD-Russia + -3']
    ('adiciu dolaran kurzon kaj 1000', ['USD-Russia']),  # TODO correct: ['USD-Russia + 1000]
    ('multigu trion kaj kvaron', ['3 * 4']),
    # Синонимы
    ('malmultigu dolaran kurzon kaj trion', ['3']),  # TODO correct: ['USD-Russia / 3']
    ('malobligu dolaran kurzon kaj trion', ['3']),  # TODO correct: не помню перевод obligu

    # ('montru dolaran kurzon kaj trion kaj kvardek', []),
    ('montru dolaran kurzon kaj trion kaj kvardekon', ['USD-Russia', '3', '40']),
    ('trion adiciu', ['3']),

    ('montru dolaran kurzon de kvarcent sesdek mil tricent dek du', ['USD-Russia']),  # TODO correct: не знаю, как нужно
    # ('montru dolaran kurzon de dua banko', []),
    # ('montru dolaran kurzon de triiliono', []),
    # ('montru dolaran kurzon de 2 banko', []),
    # ('montru dolaran kurzon de du', []),
    # ('montru dolaran kurzon de okdek', []),
    # ('montru dolaran kurzon de dek du', []),
]
""" TODO:
В примерах должна присутствовать такая последловательность:
1. Пробуем обратитьс по несуществующему синониму (или обратиться к факту. Ответ будет о не знании синонима (факта)
2. Вводим предложение, которые заносит данные в базу (факты, синонимы и так далее).
3. Пробуем вести предложение из шага 1 повторно. Ответ должен быть дан, т. к. программа теперь знает синониме (факте).
"""

import unittest

from manspy import API, Settings
from manspy import create_bd_file



TEST_INPUT_DATAS = {
    'esperanto': TEST_INPUT_DATA_ESPERANTO
}


class TestManSPy(unittest.TestCase):
    def test_manspy(self):
        def read_text(r_text, any_data):
            input_data, language = any_data
            answers[language][input_data].append(r_text)

        answers = {}
        answers_true = {}

        api = API()
        for language, test_input_data in TEST_INPUT_DATAS.items():
            settings = Settings(read_text=read_text, language=language, answer_type='construct')
            settings.db_sqlite3 = create_bd_file(settings.language, 'main_data.db')
            answers.setdefault(language, {})
            answers_true.setdefault(language, {})
            for input_data, true_answer in test_input_data:
                if input_data not in answers:
                    answers[language][input_data] = []
                if input_data not in answers_true:
                    answers_true[language][input_data] = [true_answer, input_data]
                    print()
                api.write_text(input_data, settings, {'any_data': [input_data, language]})

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