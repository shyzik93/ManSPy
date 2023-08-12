# -*- coding: utf-8 -*-
import json

from manspy.utils import unit
from manspy.api import API
from manspy.utils.constants import CASE, CATEGORY, CLASS, COORDINATING, DERIVATIVE, MOSENTENCE, NUMBER, POSPEECH
from manspy.utils.settings import Settings

TEMPLATE_HTML_WORD = '<span class="{MOSentence}" title="{title}">{word}</span>'
TEMPLATE_HTML_ROW = '{direction} &nbsp;&nbsp; {indent}{text}<br>\n'
HTML_FOOTER = '</body></html>'
HTML_HEADER = '''<!DOCTYPE html>
<html lang="ru"><head>
    <meta charset="utf-8">
</head><body>
    <style>
        .supplement {
            color: #007df8;
         }
         .subject {
         }
         .direct_supplement {
             color: blue;
         }
         .predicate {
             color: green;
         }
         .circumstance {
             color: #d6d600;
         }
         .definition {
             color: #bf8419;
         }
    </style>

    <p style="text-align:center;">
        <a target="blank" href="https://github.com/shyzik93/ManSPy"><img src="http://dosmth.ru/media/manspy_logo3.png"></a>
    </p>

    <ul style="float:right;">
        <li class="supplement">supplement (дополнение)</li>
        <li class="direct_supplement">direct supplement (прямое дополнение)</li>
        <li class="predicate">predicate (сказуемое)</li>
        <li class="circumstance">circumstance (обстоятельство)</li>
        <li class="definition">definition (определение)</li>
        <li>not member of sentence <br> (не является членом предложения)</li>
    </ul>
'''


def word_to_html(word):
    properties = [
        'base',
        CASE,
        NUMBER,
        MOSENTENCE,
        POSPEECH,
        'end',
        'end_orig'
        'end_pmark',
        'start_pmark',
        'around_pmark',
        CATEGORY,
        'give_case',
        COORDINATING,
        DERIVATIVE,
        'antonym',
        'number_value',
        CLASS,
    ]
    title = []
    for prop in properties:
        value =word[prop]
        if not value:
            continue
        title.append('{}: {}'.format(prop, value))

    return TEMPLATE_HTML_WORD.format(
        word=word['word'] + word['end'],
        MOSentence=word[MOSENTENCE].replace(' ', '_') if MOSENTENCE in word else '',
        title='\n'.join(title)
    )


def text_to_html(text, synt_words, direction):
    """ Сейчас выходной текст явлется строкой, но когда он станет классом,
        то мы уберём данное условие (подусловный блок останется)"""
    if direction == "W":
        text_ = []
        for index_sentence, cSentence in text:
            for index, cWord in cSentence:
                if 'feature' in cWord:
                    for cWord_feature in cWord['feature']:
                        text_.insert(cWord_feature['index'], word_to_html(cWord_feature))
                if cWord['index'] in synt_words:
                    cWord = synt_words[cWord['index']]
                    text_.append(word_to_html(cWord))

        return ' '.join(text_)
    return text


# TODO: добавить в лог: `ifname`, `date_recieved` (по аналогии с `make_dialog_plain_line`)
def make_dialog_html_line(text: str, direction: str):
    return TEMPLATE_HTML_ROW.format(
        indent="&nbsp;"*8 if direction == 'R' else '',
        text=text,
        direction=direction
    )


api = API()
c, cu = Settings.c, Settings.cu

with open('history.html', 'w', encoding='utf-8') as f:

    f.write(HTML_HEADER)

    rows = cu.execute('SELECT * FROM `log_history`')# WHERE `a_graphmath` IS NOT NULL')
    for row in rows:

        row = dict(row)

        if row['direction'] == 'W':

            if not row['a_synt']:
                continue
            a_graphmath_dict = json.loads(row['a_graphmath'])
            row['a_graphmath'] = unit.Text({})
            row['a_graphmath'].import_unit(a_graphmath_dict)
            row['a_morph'] = json.loads(row['a_morph'])
            row['a_postmorph'] = json.loads(row['a_postmorph'])
            a_synt_dict = json.loads(row['a_synt'])
            row['a_synt'] = unit.Text({})
            row['a_synt'].import_unit(a_synt_dict)

            #print(row['a_graphmath'][0])

            # row['_message_nl'] = ''
            # for index, sentence in row['a_graphmath']:
            #     print(index, sentence)
            #     for _index, word in sentence:
            #         _word = ObjUnit.Sentence(row['a_synt'][str(index)]).getByProperty('^', index=str(word['index']))
            #
            #        if str(_index) in row['a_synt'][str(index)]: word = ObjUnit.Sentence(row['a_synt'][str(index)])(int(_index))
            #         if _word: # слова внутри свойств не превратились в объекты слова
            #             word = ObjUnit.Word(_word[0]) if isinstance(_word[0], dict) else _word[0]
            #
            #         row['_message_nl'] += """ <span onclick="show_word_data(this)" class="word{MOSentence}" data-word='{data_word}'>{word}</span>""".format(
            #             word=word['word']+word['end_orig'],
            #             data_word=json.dumps(word.getUnit('dict'), sort_keys=True, indent=4).replace('"', ''),
            #             MOSentence=' '+word[MOSENTENCE].replace(' ', '_') if MOSENTENCE in word else ''
            #         )

            # row['a_graphmath'] = json.dumps(row['a_graphmath'].getUnit('dict'), sort_keys=True, indent=4).replace('"', '')
            # row['a_morph'] = json.dumps(row['a_morph'], sort_keys=True, indent=4).replace('"', '')
            # row['a_postmorph'] = json.dumps(row['a_postmorph'], sort_keys=True, indent=4).replace('"', '')
            # row['a_synt'] = json.dumps(row['a_synt'], sort_keys=True, indent=4).replace('"', '')

            # f.write(INTERACTIVE_HTML_LINE.format(
            #     row=row,
            #     space="&nbsp;"*(3-len(str(row['message_id']))))
            # )

            synt_words = {}
            for index_sentence, sentence in row['a_synt']:
                for index, word in sentence:
                    synt_words[word['index']] = word
                    if 'feature' in word:
                        for feature_word in word['feature']:
                            synt_words[feature_word['index']] = feature_word

            text = text_to_html(row['a_graphmath'], synt_words, row['direction'])
            text = make_dialog_html_line('{} ({})'.format(text, row['message_nl']), row['direction'])
        else:
            text = make_dialog_html_line(row['message_nl'], row['direction'])

        f.write(text)

    f.write(HTML_FOOTER)
