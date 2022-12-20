from manspy.analyzers import (
    esperanto_graphemathic,
    esperanto_morphological,
    esperanto_postmorphological,
    esperanto_syntax,
    extractor,
    converter_python,
    executor_python,
)
from manspy.utils.pipeliner import pipeliner, PipelinerGetter
from manspy.utils.message import Message
# from manspy.utils.settings import Settings
# from manspy.database.database_sqlite3 import Database

PIPELINE = PipelinerGetter([
    ('graphmath', esperanto_graphemathic),
    ('morph', esperanto_morphological),
    ('postmorph', esperanto_postmorphological),
    ('synt', esperanto_syntax),
    ('extract', extractor),
    ('convert', converter_python),
    ('exec', executor_python),
])

# Settings.database = Database(path=':memory')


def runner(text, settings, pipeline=None, any_data=None):
    pipeline = PIPELINE if pipeline is None else pipeline
    if isinstance(pipeline, str):
        pipeline = PIPELINE[pipeline]

    message = Message(settings, text, any_data=any_data)
    return pipeliner(message, pipeline)
