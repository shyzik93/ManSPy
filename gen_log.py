# -*- coding: utf-8 -*-
import json, sqlite3 as sql
from ManSPy.NLModules import ObjUnit
from manspy.utils.beautifull_repr_data import (
    INTERACTIVE_HTML_LINE, INTERACTIVE_HTML_FOOTER
)

c = sql.connect('../DATA_BASE/Esperanto/main_data.db')
c.row_factory = sql.Row
cu = c.cursor()

with open('../DATA_BASE/Esperanto/history.html', 'w') as f:

    rows = cu.execute('SELECT * FROM `log_history`')
    for row in rows:

        row = dict(row)

        row['a_graphemath'] = ObjUnit.Text(json.loads(row['a_graphemath']))
        row['a_morph'] = json.loads(row['a_morph'])
        row['a_postmorph'] = json.loads(row['a_postmorph'])
        row['a_synt'] = json.loads(row['a_synt'])

        row['_message_nl'] = '';
        for index, sentence in row['a_graphemath']:
            for _index, word in sentence:
                _word = ObjUnit.Sentence(row['a_synt'][str(index)]).getByProperty('^', index=str(word['index']))

                #if str(_index) in row['a_synt'][str(index)]: word = ObjUnit.Sentence(row['a_synt'][str(index)])(int(_index))
                if _word: # слова внутри свойств не превратились в объекты слова
                	word = ObjUnit.Word(_word[0]) if isinstance(_word[0], dict) else _word[0]

                row['_message_nl'] += """ <span onclick="show_word_data(this)" class="word{MOSentence}" data-word='{data_word}'>{word}</span>""".format(
                	word=word['word']+word['end_orig'],
                	data_word=json.dumps(word.getUnit('dict'), sort_keys=True, indent=4).replace('"', ''),
                	MOSentence=' '+word['MOSentence'].replace(' ', '_') if 'MOSentence' in word else ''
                )

        row['a_graphemath'] = json.dumps(row['a_graphemath'].getUnit('dict'), sort_keys=True, indent=4).replace('"', '')
        row['a_morph'] = json.dumps(row['a_morph'], sort_keys=True, indent=4).replace('"', '')
        row['a_postmorph'] = json.dumps(row['a_postmorph'], sort_keys=True, indent=4).replace('"', '')
        row['a_synt'] = json.dumps(row['a_synt'], sort_keys=True, indent=4).replace('"', '')

        f.write(INTERACTIVE_HTML_LINE.format(row=row, space="&nbsp;"*(3-len(str(row['message_id'])))))

    f.write(INTERACTIVE_HTML_FOOTER)
