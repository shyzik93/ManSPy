TEMPLATE_PLAIN_ROW = '* {direction}  {date_recieved}  {ifname}:  {indent}{text}\n'

class LoggerPlainText:
    file_name = 'history.html'

    def __init__(self):

    def make_dialog_plain_line(text: str, direction: str, ifname: str):
        return TEMPLATE_PLAIN_ROW.format(
            indent=' '*3 if direction == 'R' else '',
            text=text,
            direction=direction,
            date_recieved=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),#, time.gmtime(time.time()-time.altzone)),
            ifname=ifname
        )
        

        