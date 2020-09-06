import datetime
import time

TEMPLATE_HTML_WORD = '<span class="{MOSentence}">{word}</span>'
TEMPLATE_HTML_ROW = '{direction} &nbsp;&nbsp; {indent}{text}<br>\n'

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

INTERACTIVE_HTML_HEADER = '''<!DOCTYPE html>
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

            background: rgba(255, 239, 239, 0.95);
            border-left: 1px solid #e8b0b0;

            display: none;
        }

        .btn_close {
            width: 25px;
            height: 25px;
            cursor: pointer;
            border-radius: 5px;
            text-align: center;
        }
        .btn_close:hover {
            background: #efcfcf;
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
    </style>

	<script>
	    function toggle(el) {
            if (getComputedStyle(el).display == 'none') el.style.display = 'block';
            else el.style.display = 'none';
	    }

		function showNotification(message) {
		    document.getElementById('notification').children[1].innerHTML = message;
		    document.getElementById('notification').style.display = 'block';
		}

	    function show_word_data(word_el) {
            showNotification("<pre>"+ word_el.dataset.word +"</pre>");
	    }
	</script>

    <div id="notification">
        <div class='btn_close' onclick="this.parentElement.style.display = 'none';">X</div>
        <div id='notif_body'></div>
    </div>

	<ul class='main_table'>
'''

INTERACTIVE_HTML_LINE_HEADER = '''<li>
    <span class='title'>
       <span onclick="toggle(document.getElementById('more{message_id}'))"> {space}{message_id} &nbsp;&nbsp; {direction} &nbsp;&nbsp; {thread_name} &nbsp;&nbsp; {language} &nbsp;&nbsp; {date_add} </span>
       &nbsp;&nbsp; {text}
    </span>
    <ul class="more" id="more{message_id}">
'''

INTERACTIVE_HTML_LINE_FOOTER = '''    </ul>
'''

INTERACTIVE_HTML_LINE = '''
        <li>
            <span onclick="toggle(document.getElementById('data_a_graphmath{row[message_id]}'))">Графематический анализ</span><br>
            <pre class="data" id="data_a_graphemath{row[message_id]}">{row[a_graphmath]}</pre>
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
'''

INTERACTIVE_HTML_FOOTER = '</ul></body></html>'
HTML_FOOTER = '</body></html>'

def word_to_html(word):
    return TEMPLATE_HTML_WORD.format(
        word=word['word'] + word['end'],
        MOSentence=word['MOSentence'].replace(' ', '_') if 'MOSentence' in word else ''
    )

def text_to_html(text, synt_words, direction):
    """ Сейчас выходной текст явлется строкой, но когда он станет классом,
        то мы уберём данное условие (подусловный блок останется)"""
    if direction == "W":
        text_ = []
        for index_sentence, cSentence in text:
            for index, cWord in cSentence:
                # TODO: index должен равняться cWord['index']
                if cWord['index'] in synt_words:
                    cWord = synt_words[cWord['index']]
                text_.append(word_to_html(cWord))
                # if 'feature' in cWord:
                #     for cWord_feature in cWord['feature']:
                #         text_.insert(cWord_feature['index'], word_to_html(cWord_feature))
        return ' '.join(text_)
    return text

# TODO: добавить в лог: `ifname`, `date_recieved` (по аналогии с `make_dialog_plain_line`)
def make_dialog_html_line(text: str, direction: str):
    return TEMPLATE_HTML_ROW.format(
        indent="&nbsp;"*8 if direction == 'R' else '',
        text=text,
        direction=direction
    )

# TODO: Удалить функцию
def safe_results(l, space='', s=''):
    ''' удобно сохраняет список словарей или словарь словарей'''

    if isinstance(l, dict):
        l = list(l.values())

    for index, res in enumerate(l):
        if isinstance(res, (int, str)):
            s += space + str(res) + '\n'
            continue
        for k, v in res.items():
            s += space + k + ' : '
            if isinstance(v, list):
                safe_results(v, space+'    ', s+'\n')
                continue
            s += str(v) + '\n'
        if index != len(l)-1: s += '\n'
    return s
    
