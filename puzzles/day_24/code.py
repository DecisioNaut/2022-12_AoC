from __future__ import annotations

from __future__ import annotations
from typing import List, Set


def get_data(file: str):
    with open("./puzzles/day_24/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


class Pos:
    def __init__(self, row: int, col: int, time: int = 0) -> None:
        self.__row = row
        self.__col = col
        self.__time = time

    def __str__(self) -> str:
        return f"Pos({self.row}, {self.col}, {self.time})"

    __repr__ = __str__

    def __eq__(self, other: Pos) -> bool:
        return self is other

    def __hash__(self) -> int:
        return hash(id(self))

    @property
    def row(self) -> int:
        return self.__row

    @property
    def col(self) -> int:
        return self.__col

    @property
    def time(self) -> int:
        return self.__time

    @property
    def near(self) -> Set[Pos]:
        return set(
            [
                Pos(self.__row, self.__col, self.__time + 1),
                Pos(self.__row - 1, self.__col, self.__time + 1),
                Pos(self.__row + 1, self.__col, self.__time + 1),
                Pos(self.__row, self.__col - 1, self.__time + 1),
                Pos(self.__row, self.__col + 1, self.__time + 1),
            ]
        )


class Hike:
    # area: Area
    # start: Pos
    # end: Pos
    # winds: Set[Wind]
    ...


def part1(file: str) -> None:
    print(
        "Part 1:",
    )


def part2(file: str) -> None:
    print(
        "Part 2:",
    )


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("example.txt")
