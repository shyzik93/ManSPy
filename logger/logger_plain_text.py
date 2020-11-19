import datetime
import json

TEMPLATE_PLAIN_ROW = '* {direction}  {date_recieved}  {ifname}:  {indent}{text}\n'

def make_dialog_plain_line(text: str, direction: str, ifname: str):
    return TEMPLATE_PLAIN_ROW.format(
        indent=' '*3 if direction == 'R' else '',
        text=text,
        direction=direction,
        date_recieved=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),#, time.gmtime(time.time()-time.altzone)),
        ifname=ifname
    )


class LoggerPlainText:
    def __init__(self):
        self.f_history = open('history.txt', 'ab')
    
    def on_create_message(self, direction, msg):
        pass

    def log(self, direction, text, msg):
        self.f_history.write(bytearray(make_dialog_plain_line(text, direction, msg.settings.ifname), 'utf-8'))

    def before_analyzes(self, levels, msg):
        with open('analysis.txt', 'a', encoding='utf-8') as f:
            f.write('\n\n'+'#'*100+'\n')
            f.write(levels+'\n')

    def before_analysis(self, level, msg):
        now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        with open('analysis.txt', 'a', encoding='utf-8') as f:
            f.write('----'+now+'\n')
            #f.fwrite('Folding sentence: '+str(sentence.getUnit('str'))+'\n')
            f.write(('- '*10)+level+(' -'*10)+u'\n')

    def after_analysis(self, level, sentences, msg):
        if level == "graphmath":
            with open('analysis.txt', 'a', encoding='utf-8') as f:
                f.write('NL-sentence: ')
                for index, sentence in sentences:
                    for index, word in sentence.subunits_copy.items():
                        f.write(word['word']+' ')
                f.write('\n')
            sentences = sentences.getUnit('dict')
        elif level == 'morph':
            with open('comparing_fasif.txt', 'a', encoding='utf-8') as flog:
                flog.write('\n')
                for index, sentence in sentences:
                    flog.write('sentence: %s\n' % sentence.getUnit('str')['fwords'])
                flog.write('\n')

            sentences = sentences.getUnit('dict')            
        elif level == 'postmorph':
            sentences = sentences.getUnit('dict')
        elif level == 'synt':
            sentences = sentences.getUnit('dict')
        elif level == 'extract':
            sentences = list(sentences)
            return
        elif level == 'convert':
            _res = []
            for index, ILs in sentences.items():
                for IL in ILs:
                    _res.append('IL-sentence: '+str(IL))
            sentences = _res

        with open('analysis.txt', 'a', encoding='utf-8') as f: 
            json.dump(sentences, f, sort_keys=True, indent=4)#.replace('"', '')
            f.write('\n')

    def close(self):
        self.f_history.close()
