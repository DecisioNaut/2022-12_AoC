from __future__ import annotations

from typing import List, Tuple
from itertools import accumulate
from functools import partialmethod
from copy import deepcopy


def get_data(file: str) -> List[List[int]]:
    data = []
    with open("./puzzles/day_08/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            data.append([int(item) for item in line.strip()])
    return data


class HeightGrid:
    def __init__(self, data: List[List[int]]) -> None:
        self._data = data
        self._height = len(data)
        self._width = len(data[0])

    def __lt__(self, other: HeightGrid) -> BooleanGrid:
        resulting_data = deepcopy(self._data)
        for i in range(self._height):
            for j in range(self._width):
                resulting_data[i][j] = self._data[i][j] < other._data[i][j]
        return BooleanGrid(data=resulting_data)

    def view_from_top(self) -> HeightGrid:
        resulting_data = deepcopy(self._data)
        for i in range(self._height):
            print("here")
            resulting_data[:][i] = accumulate(self._data[:][i], max)
        return HeightGrid(resulting_data)

    def view_from_bottom(self) -> HeightGrid:
        resulting_data = deepcopy(self._data)
        # for i in range(self._height):
        #    for j in range(self._width):
        #        resulting_data[i][j] = self._data[i][j]
        return HeightGrid(resulting_data)

    def view_from_left(self) -> HeightGrid:
        resulting_data = deepcopy(self._data)
        # for i in range(self._height):
        #    for j in range(self._width):
        #        resulting_data[i][j] = self._data[i][j]
        return HeightGrid(resulting_data)

    def view_from_right(self) -> HeightGrid:
        resulting_data = deepcopy(self._data)
        # for i in range(self._height):
        #    for j in range(self._width):
        #        resulting_data[i][j] = self._data[i][j]
        return HeightGrid(resulting_data)

    def __str__(self) -> None:
        return str(self._data)


class BooleanGrid:
    def __init__(self, data: List[List[bool]]) -> None:
        self._data = data
        self._height = len(data)
        self._width = len(data[0])

    def __and__(self, other: BooleanGrid) -> BooleanGrid:
        resulting_data = deepcopy(self._data)
        for i in range(self._height):
            for j in range(self._width):
                resulting_data[i][j] = self._data[i][j] & other._data[i][j]
        return BooleanGrid(data=resulting_data)

    def __str__(self) -> None:
        return str(self._data)

    def count_truevals(self) -> int:
        result = 0
        for i in range(self._height):
            for j in range(self._width):
                result += self._data[i][j]
        return result


def main():
    data = get_data("part_1_data_example_2.txt")

    grid = HeightGrid(data)

    print(grid)
    print(grid.view_from_top())

    answer_part_1 = (
        (grid < grid.view_from_top())
        & (grid < grid.view_from_bottom())
        & (grid < grid.view_from_left())
        & (grid < grid.view_from_right())
    ).count_truevals()

    print("Part 1:", answer_part_1)


if __name__ == "__main__":
    main()
