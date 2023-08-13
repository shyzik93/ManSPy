class ListOfSubunits:
    """Класс для взаимодействия со списком индексов слов как со списком слов"""
    def __init__(self, parent_unit: 'import manspy.utils.base_unit.BaseUnit', list_of_indexes: list):
        """
        :param parent_unit:
        :param list_of_indexes:
        """
        self.unit = parent_unit
        self.indexes = list_of_indexes

    def __getitem__(self, position: int):
        return self.unit.subunit_info[self.indexes[position]]

    def __iter__(self):
        for index in self.indexes:
            yield self.unit.subunit_info[index]

    def __bool__(self):
        return bool(self.indexes)

    def append(self, subunit: 'import manspy.utils.base_unit.BaseUnit'):
        self.indexes.append(subunit)
