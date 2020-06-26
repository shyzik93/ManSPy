import os.path
import time
import datetime
import json

class History:
    def __init__(self):
         if not os.path.exists('history.html'): self.html_head()

    def plain(self, sText, direction, IFName):
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()-time.altzone))
        if direction == 'R': sText = '   '+sText
        sText = "* %s  %s  %s: %s\n" % (direction, Time, IFName, sText)
        with open('history.txt', 'ab') as f: f.write(bytearray(sText, 'utf-8'))

    def html_head(self):
        with open('history.html', 'w') as f:
            f.write("""<!DOCTYPE html>
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

""")

    def html_row(self, sText, direction):
        with open('history.html', 'a') as f:
            f.write("""    {0} &nbsp;&nbsp; {1}<br>""".format(direction, sText))

    def html_build_word(self, cWord):
        return """<span class="word{MOSentence}">{word}</span>""".format(
            word=cWord['word'] + cWord['end'],
            MOSentence=' '+cWord['MOSentence'].replace(' ', '_') if 'MOSentence' in cWord else ''
        )

    def html_build_text(self, cText):
        text_ = []

        for index, cSentence in cText:
            for index, cWord in cSentence.subunits_copy.items():
                text_.append(self.html_build_word(cWord))

        return ' '.join(text_)

    def html(self, mText, direction):
        if direction == "W": self.html_row(self.html_build_text(mText), direction)
        else: self.html_row("&nbsp;"*8 + mText, direction)


    def log(self, title, res):

        if title == "graphmath":
            with open('analysis.txt', 'a', encoding='utf-8') as f:
                f.write('NL-sentence: ')
                for index, sentence in res:
                    for index, word in sentence.subunits_copy.items(): f.write(word['word']+' ')
                f.write('\n')
            res = res.getUnit('dict')
        elif title == 'morph':
            pass
            with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
                flog.write('\n')
                for index, sentence in res: flog.write('sentence: %s\n' % sentence.getUnit('str')['fwords'])
                flog.write('\n')

            res = res.getUnit('dict')            
        elif title == 'postmorph':
            res = res.getUnit('dict')
        elif title == 'synt':
            self.html(res, 'W')
            res = res.getUnit('dict')
        elif title == 'extract':
            res = list(res)
            return
        elif title == 'convert':
            _res = []
            for index, ILs in res.items():
                for IL in ILs:
                    _res.append('IL-sentence: '+str(IL))
            res = _res

        now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        with open('analysis.txt', 'a', encoding='utf-8') as f:
            f.write('----'+now+'\n')
            #f.fwrite('Folding sentence: '+str(sentence.getUnit('str'))+'\n')
            f.write(('- '*10)+title+(' -'*10)+u'\n')

            json.dump(res, f, sort_keys=True, indent=4)#.replace('"', '')
            f.write('\n')

    def header(self, levels):
        with open('analysis.txt', 'a', encoding='utf-8') as f:
            f.write('\n\n'+'#'*100+'\n')
            f.write(levels+'\n')
