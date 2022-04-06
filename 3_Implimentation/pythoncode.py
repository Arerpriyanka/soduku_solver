import copy
from typing import List, Set, Tuple


class Cell(object):
    MAX_VALUE = 9  # TODO rethink if it should be class static

    def __init__(self, row: int, column: int, editable=True, value=0):

        if editable is False and value == 0:
            raise AttributeError("Cell not editable and without value")
        elif value < 0 or value > self.MAX_VALUE:
            raise AttributeError("Incorrect value ({} not in <0,{}>)".format(value, self.MAX_VALUE))
        elif not(0 <= row < self.MAX_VALUE) or not(0 <= column < self.MAX_VALUE):
            raise AttributeError("Incorrect row or column ({},{} not in <0,{}>".format(row, column, self.MAX_VALUE))

        self._editable = editable
        self._value = value
        self._row = row
        self._column = column

        if editable:
            self._possible_values = set(range(1, self.MAX_VALUE + 1))
        else:
            self._possible_values = set()

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def editable(self) -> bool:
        return self._editable

    @property
    def possible_values(self) -> Set[int]:
        return self._possible_values

   
