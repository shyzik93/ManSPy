import unittest
import sys

from unittest.mock import patch

from manspy.cli import do_cmd

TEST_ARG_LISTS = [
    (['--text', 'montru dolran kurzon'], [])
]

outputs = []


def mock_print(*args):
    outputs.extend(args)


class TestCLI(unittest.TestCase):

    @patch('manspy.cli.print', mock_print)
    def test_cli(self):
        def stdout(output):
            print('out:', output)

        source_stdout = sys.stdout

        for args_list, answers in TEST_ARG_LISTS:
            #sys.stdout = stdout
            do_cmd(args_list)
            print(outputs)
            #sys.stdout = source_stdout
            #self.assertEqual(True, False)


