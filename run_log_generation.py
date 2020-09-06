# -*- coding: utf-8 -*-
import json
import sqlite3 as sql

from manspy.NLModules import ObjUnit
from manspy.utils.beautifull_repr_data import (
    HTML_HEADER,
    TEMPLATE_HTML_WORD,
    TEMPLATE_HTML_ROW,
    HTML_FOOTER,
    INTERACTIVE_HTML_HEADER,
    INTERACTIVE_HTML_LINE,
    INTERACTIVE_HTML_FOOTER,
    text_to_html,
    make_dialog_html_line
)

c = sql.connect('../DATA_BASE/esperanto/main_data.db')
c.row_factory = sql.Row
cu = c.cursor()

with open('../DATA_BASE/esperanto/history.html', 'w', encoding='utf-8') as f:

    f.write(HTML_HEADER)

    rows = cu.execute('SELECT * FROM `log_history`')# WHERE `a_graphmath` IS NOT NULL')
    for row in rows:

        row = dict(row)

        if row['direction'] == 'W':

            a_graphmath_dict = json.loads(row['a_graphmath'])
            row['a_graphmath'] = ObjUnit.Text({})
            row['a_graphmath'].import_unit(a_graphmath_dict)
            row['a_morph'] = json.loads(row['a_morph'])
            row['a_postmorph'] = json.loads(row['a_postmorph'])
            a_synt_dict = json.loads(row['a_synt'])
            row['a_synt'] = ObjUnit.Text({})
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
            #             MOSentence=' '+word['MOSentence'].replace(' ', '_') if 'MOSentence' in word else ''
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
