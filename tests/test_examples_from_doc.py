import unittest
import os.path
import re

from manspy.utils.settings import Settings, InitSettings
from manspy.runners.simple import runner

REGEXP_MARKDOWN_LINK = r'\[([^\]]+)\]\(https://syeysk.ru/api/manspy/run_get\?s=([\w/%\d]+)\)[^>]+((?:<span>`[\w\s\d]+`</span>[\s\w]*)+)'


def collect_examples(doc_path):
    with open(doc_path, 'r', encoding='utf-8') as fdoc:
        match = re.findall(REGEXP_MARKDOWN_LINK, fdoc.read())
        for sentence, encoded_sentence, answer in match:
            decoded_sentence = encoded_sentence.replace('%20', ' ')
            if decoded_sentence == sentence:
                yield sentence, re.findall(r'<span>`([\s\w\d]+)`</span>', answer)


class ExamplesFromDocTestCase(unittest.TestCase):
    def test_examples(self):
        gen_examples = collect_examples(os.path.join(os.path.dirname(__file__), '../DOC/Theory.md'))
        settings = Settings(answer_type='fake', history=False)
        with InitSettings():
            for sentence, expecting_answer in gen_examples:
                with self.subTest():
                    settings.language = 'esperanto'
                    r_texts = runner(sentence, settings)
                    r_texts = [str(r_text) if isinstance(r_text, int) else r_text for r_text in r_texts]
                    self.assertListEqual(r_texts, expecting_answer, sentence)
