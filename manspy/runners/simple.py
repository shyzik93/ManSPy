from manspy.analyzers import (
    esperanto_graphemathic,
    esperanto_morphological,
    esperanto_postmorphological,
    esperanto_syntax,
    extractor,
    converter,
    executor_internal_sentences,
)
from manspy.utils.pipeliner import pipeliner
from manspy.utils.message import Message  # from manspy.utils.message import Message
#from manspy.utils.settings import Settings

PIPELINE = [
    esperanto_graphemathic,
    esperanto_morphological,
    esperanto_postmorphological,
    esperanto_syntax,
    extractor,
    converter,
    executor_internal_sentences,
]


def runner(text, settings, pipeline=None):
    pipeline = PIPELINE if pipeline is None else pipeline
    message = Message(settings, text)
    return pipeliner(message, pipeline)
