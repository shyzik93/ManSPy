from manspy.runners.simple_python import runner
from manspy.utils.settings import Settings, InitSettings

settings = Settings(send_to_out=lambda x, any_data: print(x, any_data))

with InitSettings():
    for sentence in runner('adiciu dolaran kurzon kaj tria kvin', settings):
        print(sentence)

    for sentence in runner('sxaltu tablan lampon en dormcxambro', settings):
        print(sentence)