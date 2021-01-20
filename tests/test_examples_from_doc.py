import unittest
import os.path
import re

from manspy import API, Settings

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
        def send_to_out(r_text, arg0):
            r_texts.append(r_text)

        r_texts = []
        gen_examples = collect_examples(os.path.join(os.path.dirname(__file__), '../DOC/Theory.md'))
        settings = Settings(send_to_out=send_to_out, answer_type='fake', history=False)
        with API() as api:
            for sentence, expecting_answer in gen_examples:
                with self.subTest():
                    settings.language = 'esperanto'
                    api.send_to_in(sentence, settings)
                    self.assertListEqual(r_texts, expecting_answer, sentence)
                    r_texts.clear()


