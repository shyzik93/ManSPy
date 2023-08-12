from manspy.utils.unit.base_unit import BaseUnit


class Text(BaseUnit):
    """ Класс объекта ткста.
        Возможности: анализ, обработка (изменение времени, стиля текста (публистический, официальный) и прочее)
    """
    def __init__(self, sentences, parent=None):
        BaseUnit.__init__(self, sentences, parent_object={'name': 'text', 'value': self}, parent=parent)
