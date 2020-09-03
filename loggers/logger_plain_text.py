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
        self.f = open('history.txt', 'ab')
    
    def log(self, direction, msg, settings):
        self.f.write(bytearray(make_dialog_plain_line(text, direction, ifname), 'utf-8'))
        