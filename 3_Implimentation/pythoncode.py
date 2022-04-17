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

   @property
    def value(self) -> int:
        return self._value
    @value.setter
    def value(self, value: int):
        if self._editable is False:
            raise AttributeError("Cell not editable")
        elif value < 0 or value > self.MAX_VALUE:
            raise AttributeError("Incorrect value ({} not in <0,{}>)".format(value, self.MAX_VALUE))
        elif value == 0:
            self._value = value
        else:
            self._value = value
            self._possible_values.clear()

    def init_possible_values(self):
        self._possible_values = set(range(1, 1+self.MAX_VALUE))

    def intersect_possible_values(self, values: set):
        self._possible_values = self._possible_values.intersection(values)

    def clear(self):
        if self.editable:
            self.value = 0

    def remove_possible_value(self, value: int):
        if value in self._possible_values:
            self._possible_values.remove(value)
    def to_string(self) -> str:
        return "[{0._row},{0._column}]: editable: {0._editable}: {0._value} / {0._possible_values}".format(self)

class Region(object):
    def __init__(self):
        self._cells = []

    @property
    def cells(self):
        return self._cells

    def add(self, cell: Cell):
        """Add a cell to a list of cells if the list does not contain it.

        Args:
            cell (Cell): Cell to be added to the list.
        """
        if cell not in self._cells:
            self._cells.append(cell)

    def remove_possible_value_if_cell_is_in_region(self, cell: Cell, value: int):

        if cell in self._cells:
            for cell in self._cells:
                cell.remove_possible_value(value)

    def update_possible_values(self):
        values = set(range(1, 1+len(self._cells)))
        for cell in self._cells:
            v = cell.value
            if v in values:
                values.remove(v)

        for cell in self._cells:
            if cell.value == 0:
                cell.intersect_possible_values(values)

    def is_solved(self) -> bool:
        values = set()
        for cell in self._cells:
            values.add(cell.value)

        expected_values = set(range(1, len(self._cells)+1))
        return values == expected_values

    def is_not_possible_to_solve(self):

        a_set = set()
        for cell in self._cells:
            if cell.value == 0 and len(cell.possible_values) == 0:
                return True
            elif cell.value in a_set:
                return True
            elif cell.value != 0:
                a_set.add(cell.value)
        return False


class UndoRedo(object):

    def __init__(self):
        self._undo = []
        self._redo = []

    def add_action(self, row: int, column: int, old_value: int, value: int, method: str = ''):

        self._undo.append((row, column, old_value, value, method))
        self._redo.clear()

    def undo_length(self):
        return len(self._undo)

    def redo_length(self):
        return len(self._redo)

    def undo(self) -> Tuple[int, int, int, int, str, int, int]:

        last_action = self._undo.pop()
        self._redo.append(last_action)
        return (last_action), len(self._undo), len(self._redo)

    def redo(self):

        redo_action = self._redo.pop()
        self._undo.append(redo_action)
        return (redo_action), len(self._undo), len(self._redo)
class Sudoku(object):
    def __init__(self, size=9, cells=None, rect_width=3, rect_height=3):
        if cells is None:
            self.cells = [[Cell(r, c) for c in range(size)] for r in range(size)]
            self._size = size
        else:
            self.cells = cells
            self._size = len(cells)

        self._undo_redo = UndoRedo()

        self._rect_width = rect_width
        self._rect_height = rect_height

        rows = columns = self._size
        rectangles = (self._size ** 2) // (self._rect_width * self._rect_height)  # number of rectangles = board size / rect_size
        self._regions = [Region() for x in range(rows + columns + rectangles)]  # generate regions for rows, cols, rects

        for row in range(self._size):
            for col in range(self._size):
                self._regions[row].add(self.cells[row][col])        # populate row regions
                self._regions[rows+col].add(self.cells[row][col])   # populate column regions

        # populate rectangle regions
        width_size = self._size // self._rect_width
        height_size = self._size // self._rect_height
        reg = self._size * 2 - 1
        for x_start in range(height_size):
            for y_start in range(width_size):
                reg += 1
                for x in range(x_start * width_size, (x_start+1) * width_size):
                    for y in range((y_start * height_size), (y_start+1) * height_size):
                        self._regions[reg].add(self.cells[x][y])

        self.update_possible_values_in_all_regions()

    @property
    def size(self) -> int:
        return self._size

    @property
    def regions(self) -> List[Region]:
        return self._regions

    def _is_row_and_column_in_range(self, row: int, column: int) -> bool:

        if (0 <= row < self.size) and (0 <= column < self.size):
            return True
        else:
            raise AttributeError("Row or column out of range: <0,{}>, ({},{})".format(self.size - 1, row, column))

    def get_cell_value(self, row: int, column: int) -> int:
        if self._is_row_and_column_in_range(row, column):
            return self.cells[row][column].value

    def set_cell_value(self, row: int, column: int, value: int, method: str = ''):
        if self._is_row_and_column_in_range(row, column):
            cell = self.cells[row][column]
            old_value = cell.value
            cell.value = value
            self._remove_possible_value(cell, value)
            self._undo_redo.add_action(row, column, old_value, value, method)

    def _remove_possible_value(self, cell: Cell, value: int):

        for region in self._regions:
            region.remove_possible_value_if_cell_is_in_region(cell, value)

    def get_cell_possibilities(self, row: int, column: int) -> Set[int]:

        if self._is_row_and_column_in_range(row, column):
            return self.cells[row][column].possible_values

    def is_editable(self, row: int, column: int) -> bool:

        if self._is_row_and_column_in_range:
            return self.cells[row][column].editable

    def update_possible_values_in_all_regions(self):

        for region in self._regions:
            region.update_possible_values()

    def is_solved(self) -> bool:

        for region in self._regions:
            if not region.is_solved():
                return False
        return True

    def is_wrong(self) -> bool:

        for region in self._regions:
            if region.is_not_possible_to_solve():
                return True
        return False

    def to_string(self) -> str:

        sudoku = ""
        for row in self.cells:
            for cell in row:
                sudoku += str(cell.value)
            sudoku += "\n"
        return sudoku

    def copy_from(self, sudoku: 'Sudoku'):

        for i in range(self._undo_redo.undo_length(), sudoku._undo_redo.undo_length()):
            row, column, old_value, value, method = sudoku._undo_redo._undo[i]
            self.set_cell_value(row, column, value, method)


class SudokuSolver(object):
    def __init__(self, sudoku: Sudoku = None):

        self.sudoku = sudoku
        self.patterns = Pattern.get_patterns_without_brute_force()

    def solve(self) -> bool:

        restart = True
        while restart:
            restart = False
            for pattern in self.patterns:
                solve_again = pattern.solve(self.sudoku, False)
                if self.sudoku.is_solved():
                    restart = False
                    break
                elif solve_again:
                    restart = True

        # If not solved by means of typical patterns - use Brute Force.
        if not self.sudoku.is_solved():
            pattern = BruteForce()
            pattern.solve(self.sudoku, False)

        return self.sudoku.is_solved()

    def to_string(self) -> str:
        return self.sudoku.to_string()

class Pattern(object):

    def solve(self, sudoku: Sudoku, solve_one: bool = False) -> bool:
        return false
