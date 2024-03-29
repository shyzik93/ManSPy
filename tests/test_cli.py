import unittest
from unittest.mock import patch

from run_cli import run

TEST_ARG_LISTS = [
    ([], []),
    (['--text', 'montru dolaran kurzon'], ['60']),
    (['--text', 'montru adreson de komputilo kaj dolaran kurzon'], ['192.168.0.1', '60']),
]

outputs = []


def mock_print(*args):
    outputs.extend(args)


class CLITestCase(unittest.TestCase):
    @patch('builtins.print', mock_print)
    def test_cli(self):
        for args_list, answers in TEST_ARG_LISTS:
            run(args_list)
            self.assertListEqual(outputs, answers, ' '.join(args_list))
            outputs.clear()
