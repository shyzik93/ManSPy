import unittest

from manspy.cli import do_cmd

TEST_ARG_LISTS = [
    (['--text', 'montru dolran kurzon'], [])
]


class TestCLI(unittest.TestCase):
    def test_cli(self):
        for args_list, answers in TEST_ARG_LISTS:
            res = do_cmd(args_list)
            print(res)
            #self.assertEqual(True, False)


