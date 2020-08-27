import time

TEMPLATE_HTML_WORD = '<span class="word{MOSentence}">{word}</span>'
TEMPLATE_HTML_ROW = '{direction} &nbsp;&nbsp; {indent}{text}<br>\n'
TEMPLATE_PLAIN_ROW = '"* {direction}  {date_recieved}  {ifname}:  {indent}{text}\n"'

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
    return TEMPLATE_HTML_WORD.format(
        word=word['word'] + word['end'],
        #MOSentence=word['MOSentence'].replace(' ', '_') if 'MOSentence' in word else ''
        MOSentence=word.get('MOSentence', '').replace(' ', '_')
    )

# TODO: добавить в лог: `ifname`, `date_recieved` (по аналогии с `make_dialog_plain_line`)
def make_dialog_html_line(text: str, direction: str):
    return TEMPLATE_HTML_ROW.format(
        indent="&nbsp;"*8 if direction == 'R' else ''
        text=text,
        direction=direction)

def make_dialog_plain_line(text: str, direction: str, ifname: str):
    return TEMPLATE_PLAIN_ROW.format(
        indent=' '*3 if direction == 'R' else ''
        text=text,
        direction=direction,
        date_recieved=time.time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()-time.altzone)),
        ifname=ifname
    )

