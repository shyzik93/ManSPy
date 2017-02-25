# -*- coding: utf-8 -*-
import json, sqlite3 as sql
from ManSPy.NLModules import ObjUnit

def safeResults(l, space='', s=''):
  ''' удобно сохраняет список словарей или словарь словарей'''

  if isinstance(l, dict):
    l2 = []
    for k, v in l.items():
      l2.append(v)
    l = l2

  for res in l:
    if isinstance(res, (int, str)):
      s += space + str(res) + '\n'
      continue
    for k, v in res.items():
      if isinstance(v, list):
        s += space + k + ' : \n'
        safeResults(v, space+'    ', s)
        continue
      s += space + k + ' : ' + str(v) + '\n'
    index = l.index(res)
    if index != len(l)-1: s += '\n'
  return s

c = sql.connect('../DATA_BASE/Esperanto/main_data.db')
c.row_factory = sql.Row
cu = c.cursor()

with open('../DATA_BASE/Esperanto/history.html', 'w') as f:
    f.write('''<!DOCTYPE html>
    	<html lang="ru"><head>
            <meta charset="utf-8">
    	</head><body>
 
		    <style>
                body {
                    font-family: non-serif "Verdana"
                }

                #notification {
                    position: fixed;
                    top:0;
                    right:0;
                    width:250px;
                    height: 100vh;
                    overflow-y:scroll;
                }

		        .more {
		            display: none;
		        }
		        .data {
		            display: none;
		        }

		        .main_table > li > .title {
                    cursor:pointer;
                    margin-top: 5px;
                    width:100%;
                    display:inline-block;
		        }
		        .main_table > li > .title:hover {
                    background: #eee;
		        }
		        .main_table .word:hover {
                    background: #ddd;
		        }
		    </style>

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
		            color: yellow
		        }
		        .definition {
		            color: #bf8419
		        }
		        /*. {
		        }
		        . {
		        }
		        . {
		        }
		        . {
		        }
		        . {
		        }
		        . {
		        }*/

		    </style>

			<script>
			    function toggle(el) {
		            if (getComputedStyle(el).display == 'none') el.style.display = 'block';
		            else el.style.display = 'none';
			    }

				function showNotification(message) {
				    document.getElementById('notification').innerHTML = message;
				}

			    function show_word_data(word_el) {
                    showNotification("<pre>"+ word_el.dataset.word +"</pre>");
			    }
			</script>

            <div id="notification"></div>

			<ul class='main_table'>''')

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
                	word=word['word'],
                	data_word=json.dumps(word.getUnit('dict'), sort_keys=True, indent=4).replace('"', ''),
                	MOSentence=' '+word['MOSentence'].replace(' ', '_') if 'MOSentence' in word else ''
                )

        row['a_graphemath'] = json.dumps(row['a_graphemath'].getUnit('dict'), sort_keys=True, indent=4).replace('"', '')
        row['a_morph'] = json.dumps(row['a_morph'], sort_keys=True, indent=4).replace('"', '')
        row['a_postmorph'] = json.dumps(row['a_postmorph'], sort_keys=True, indent=4).replace('"', '')
        row['a_synt'] = json.dumps(row['a_synt'], sort_keys=True, indent=4).replace('"', '')

        f.write('''
	        	<li>
	        	    <span class='title'>
	                   <span onclick="toggle(document.getElementById('more{row[message_id]}'))"> {space}{row[message_id]} &nbsp;&nbsp; {row[direction]} &nbsp;&nbsp; {row[thread_name]} &nbsp;&nbsp; {row[language]} &nbsp;&nbsp; {row[date_add]} </span>
	                   &nbsp;&nbsp; {row[_message_nl]}
	                </span>
	                <ul class="more" id="more{row[message_id]}">

				        <li>
				            <span onclick="toggle(document.getElementById('data_a_graphemath{row[message_id]}'))">Графематический анализ</span><br>
    			            <pre class="data" id="data_a_graphemath{row[message_id]}">{row[a_graphemath]}</pre>
				        </li><li>
				            <span onclick="toggle(document.getElementById('data_a_morph{row[message_id]}'))">Морфологический анализ</span><br>
    			            <pre class="data" id="data_a_morph{row[message_id]}">{row[a_morph]}</pre>
				        </li><li>
				            <span onclick="toggle(document.getElementById('data_a_postmorph{row[message_id]}'))">Постморфологический анализ</span><br>
    			            <pre class="data" id="data_a_postmorph{row[message_id]}">{row[a_postmorph]}</pre>
				        </li><li>
				            <span onclick="toggle(document.getElementById('data_a_synt{row[message_id]}'))">Синтаксический анализ</span><br>
    			            <pre class="data" id="data_a_synt{row[message_id]}">{row[a_synt]}</pre>
				        </li><li>
				            <span>Извлечение</span><br>
				        </li><li>
				            <span>Конвертация во ВЯ</span><br>
				        </li><li>
				            <span>Выполнение</span><br>
				        </li>

			        </ul>
			    </li>'''.format(row=row, space="&nbsp;"*(3-len(str(row['message_id'])))))

    f.write('</ul></body></html>')

['message_id', 'direction', 'thread_name', 'language', 'date_add', 'message_nl', 'message_il', 'a_graphemath', 'a_morph', 'a_postmorph', 'a_synt']