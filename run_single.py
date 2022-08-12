from manspy.analyse_text import nature2internal
from manspy.message import Message
from manspy.utils.settings import Settings, InitSettings

settings = Settings(send_to_out=lambda x, any_data: print(x, any_data))

with InitSettings():
    w_text = 'adiciu dolaran kurzon kaj tria kvin'
    r_text = nature2internal(Message(settings, w_text))
    for sentence in r_text:
        print(sentence)
