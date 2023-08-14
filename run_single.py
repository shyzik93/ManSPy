from manspy.runners.simple import runner
from manspy.utils.settings import Settings, InitSettings
from manspy.loggers.logger_db import LoggerDb
from manspy.loggers.logger_plain_text import LoggerPlainText

Settings.loggers.append(LoggerDb())
Settings.loggers.append(LoggerPlainText())

settings = Settings(send_to_out=lambda x, any_data: print(x, any_data))

with InitSettings():
    for sentence in runner('adiciu dolaran kurzon kaj tria kvin', settings):
        print(sentence)

    for sentence in runner('sxaltu tablan lampon en dormcxambro', settings):
        print(sentence)
