from manspy.utils.pipeliner import pipeliner
from manspy.utils.message import Message
from manspy.utils.settings import Settings, InitSettings

settings = Settings(send_to_out=lambda x, any_data: print(x, any_data))

with InitSettings():
    w_text = 'adiciu dolaran kurzon kaj tria kvin'
    r_text = pipeliner(Message(settings, w_text))
    for sentence in r_text:
        print(sentence)
