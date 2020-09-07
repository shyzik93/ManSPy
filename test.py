import unittest
import time

from manspy import API, create_bd_file

""" TODO:
В примерах должна присутствовать такая последловательность:
1. Пробуем обратитьс по несуществующему синониму (или обратиться к факту. Ответ будет о не знании синонима (факта)
2. Вводим предложение, которые заносит данные в базу (факты, синонимы и так далее).
3. Пробуем вести предложение из шага 1 повторно. Ответ должен быть дан, т. к. программа теперь знает синониме (факте).
"""

TEST_INPUT_DATA_ESPERANTO = [
    ('montru dolaran kaj euxran kurzon de rusia banko', ['EUR-Russia', 'USD-Russia']),
    ('sxaltu tablan lampon en dormcxambro', ['1%201%201']),
    ('montru adreson de komputilo', ['127.0.0.1']),
    ('montru adreson de androido', []),

    ('dolaran kurzon montru', ['USD-Russia']),
    ('montru de rusia banko euxran kurzon', ['EUR-Russia']),

    # Повторяющиеся аргументы (однородные слова)
    ('montru dolaran kaj dolaran kurzon de rusia banko', ['USD-Russia']),
    ('montru dolaran kaj dolaran kurzon de rusia kaj rusia banko', ['USD-Russia']),
    # Это предложение выдаёт курс доллара только по росбанку (украинский не замечает).
    # TODO: Как вариант решения: проверять каждоый однородный член у дополнений (кроме первого)
    #  (однородные члены должны совпадать по части речи)
    #('montru dolaran kurzon de rusia banko kaj ukraina banko', ['USD-Russia', 'USD-Ukrain']),
    ('montru adreson de komputilo kaj androido', ['192.168.43.167']),
    # Много аргументов (сложатся друг с другом поочерёдно - декартово произведение)
    ('montru euxran kaj dolaran kurzon de ukrainia kaj rusia kaj belarusia banko', [
        'USD-Belarus',
        'USD-Russia',
        'USD-Ukraine',
        'EUR-Belarus',
        'EUR-Russia',
        'EUR-Ukraine'
    ]),
    ('montru euxran kaj dolaran kurzon de ukrainia kaj rusia banko', []),
    # TODO: сложатся соответственно (не реализовано пока)
    ('montru euxran kaj dolaran kurzon de ukrainia kaj rusia banko соответсвенно', []),
    # TODO: однородные слова-посредники (не реализовано пока)
    ('montru dolaran kurzon de ukrainia banko kaj de rusia banko', []),
    # антонимия. Можно через приставку, которая антонимирует значение, а можно через глагол-антоним
    ('malsxaltu tablan lampon en dormcxambro kaj fermo', []),
    ('malmontru dolaran kurzon de rusia banko de mia domo', []),
    # однородные прямые дополнения, по сути - две разных функции (два разных действия) в одном предложении.
    ('montru adreson de komputilo kaj dolaran kurzon', []),
    ('montru adreson de komputilo kaj dolaran kurzon de belarusia banko', []),
    ('montru dolaran kurzon kaj adreson de komputilo', []),
    # Пунктуация
    ('montru euxran, dolaran kurzon de ukrainia banko.', []),
    ('montru euxran, dolaran kurzon de ukrainia banko .', []),
    ('montru euxran, dolaran kurzon de ukrainia banko ...', []),
    # ('Montru dolaran kurzon. Montru euxran kurzon de belarusia banko', []),
    # TODO: пока не поддерживаются
    # ('montru dolaran kurzon, kiu estas dolara', []),
    # ('Se euxra cambio de belarusia banko estas sepduk kvar, do sxaltu tablan lampon en dormcxambro', []),
    # ('Do sxaltu tablan lampon en dormcxambro, se euxra cambio de belarusia banko estas sepduk kvar', []),
    ('adiciu dudekon trion', []),
    ('adiciu kvardekon kaj trion kaj milionon', []),
    ('maladiciu dolaran kurzon kaj trion', []),
    ('adiciu dolaran kurzon kaj 1000', []),
    ('multigu trion kaj kvaron', []),
    # Синонимы
    ('malmultigu dolaran kurzon kaj trion', []),
    ('malobligu dolaran kurzon kaj trion', []),

    # ('montru dolaran kurzon kaj trion kaj kvardek', []),
    ('montru dolaran kurzon kaj trion kaj kvardekon', []),
    ('trion adiciu', []),

    ('montru dolaran kurzon de kvarcent sesdek mil tricent dek du', []),
    # ('montru dolaran kurzon de dua banko', []),
    # ('montru dolaran kurzon de triiliono', []),
    # ('montru dolaran kurzon de 2 banko', []),
    # ('montru dolaran kurzon de du', []),
    # ('montru dolaran kurzon de okdek', []),
    # ('montru dolaran kurzon de dek du', []),
]

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
            settings = api.Settings(read_text=read_text, language=language)
            settings.db_sqlite3 = create_bd_file(settings.language, 'main_data.db')
            answers.setdefault(language, {})
            answers_true.setdefault(language, {})
            for input_data, true_answer in test_input_data:
                if input_data not in answers:
                    answers[language][input_data] = []
                if input_data not in answers_true:
                    answers_true[language][input_data] = [true_answer, input_data]
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