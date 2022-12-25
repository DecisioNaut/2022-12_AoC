from __future__ import annotations
from typing import List, Optional, Dict, Union, Set
from functools import total_ordering, cache
from pprint import pprint


@total_ordering
class Pos:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __str__(self):
        return f"Pos({self.row}, {self.col})"

    __repr__ = __str__

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other: Pos) -> bool:
        return (self.row == other.row) & (self.col == other.col)

    def __lt__(self, other: Pos) -> bool:
        if self.row < other.row:
            return True
        elif self.row == other.row:
            return self.col < other.col
        else:
            return False

    @cache
    def close_posses_dict(self) -> Dict[str, Pos]:
        row, col = self.row, self.col
        return {
            "nw": Pos(row - 1, col - 1),
            "nn": Pos(row - 1, col),
            "ne": Pos(row - 1, col + 1),
            "ww": Pos(row, col - 1),
            "__": Pos(row, col),
            "ee": Pos(row, col + 1),
            "sw": Pos(row + 1, col - 1),
            "ss": Pos(row + 1, col),
            "se": Pos(row + 1, col + 1),
        }

    @cache
    def close_posses(self) -> Set[Pos]:
        return set(
            [value for key, value in self.close_posses_dict().items() if key != "__"]
        )

    @cache
    def nish_posses(self) -> Set[Pos]:
        return set(
            [value for key, value in self.close_posses_dict().items() if "n" in key]
        )

    @cache
    def n_pos(self) -> Pos:
        return self.close_posses_dict()["nn"]

    @cache
    def sish_posses(self) -> Set[Pos]:
        return set(
            [value for key, value in self.close_posses_dict().items() if "s" in key]
        )

    @cache
    def s_pos(self) -> Pos:
        return self.close_posses_dict()["ss"]

    @cache
    def wish_posses(self) -> Set[Pos]:
        return set(
            [value for key, value in self.close_posses_dict().items() if "w" in key]
        )

    @cache
    def w_pos(self) -> Pos:
        return self.close_posses_dict()["ww"]

    @cache
    def eish_posses(self) -> Set[Pos]:
        return set(
            [value for key, value in self.close_posses_dict().items() if "e" in key]
        )

    @cache
    def e_pos(self) -> Pos:
        return self.close_posses_dict()["ee"]

    @cache
    def xish_posses(self, x: str) -> Set[Pos]:
        return set(
            [value for key, value in self.close_posses_dict().items() if x in key]
        )

    @cache
    def x_pos(self, x: str) -> Pos:
        return self.close_posses_dict()[x + x]


def _doesnt_overlap(first: Union[Pos, Set[Pos]], second: Set[Pos]):
    if isinstance(first, set):
        return set.intersection(first, second) == set()
    else:
        return first not in second


@total_ordering
class Elve:

    counter = 0

    def __init__(self, pos: Pos) -> None:
        self.id = Elve.counter
        Elve.counter += 1
        self.pos: Pos = pos
        self.propos: Pos = pos
        self.next_pos: Pos = pos
        self._other_elves: Optional[List[Elve]] = None
        self._xs = ["n", "s", "w", "e"]

    @property
    def other_elves(self) -> Optional[List[Elve]]:
        return self._other_elves

    @other_elves.setter
    def other_elves(self, other_elves: List[Elve]) -> None:
        self._other_elves = other_elves

    def _get_posses_other_elves(self) -> Set[Pos]:
        return set([elve.pos for elve in self._other_elves])

    def get_propos(self) -> None:
        posses_other_elves = self._get_posses_other_elves()
        if _doesnt_overlap(self.pos.close_posses(), posses_other_elves):
            self.propos = self.pos
        elif _doesnt_overlap(self.pos.xish_posses(self._xs[0]), posses_other_elves):
            self.propos = self.pos.x_pos(self._xs[0])
        elif _doesnt_overlap(self.pos.xish_posses(self._xs[1]), posses_other_elves):
            self.propos = self.pos.x_pos(self._xs[1])
        elif _doesnt_overlap(self.pos.xish_posses(self._xs[2]), posses_other_elves):
            self.propos = self.pos.x_pos(self._xs[2])
        elif _doesnt_overlap(self.pos.xish_posses(self._xs[3]), posses_other_elves):
            self.propos = self.pos.x_pos(self._xs[3])
        else:
            self.propos = self.pos

    def _get_proposses_other_elves(self) -> Set[Pos]:
        return set([elve.propos for elve in self._other_elves])

    def get_next_pos(self) -> None:
        proposses_other_elves = self._get_proposses_other_elves()
        if _doesnt_overlap(self.propos, proposses_other_elves):
            self.next_pos = self.propos

    def get_intends_move(self) -> bool:
        return self.next_pos != self.pos

    def move_to_next_pos(self) -> None:
        self.pos, self.propos = (
            self.next_pos,
            self.next_pos,
        )
        self._xs = self._xs[1:] + [self._xs[0]]

    def __str__(self):
        return f"Elve_{str(self.id).zfill(4)} @ {self.pos}"

    __repr__ = __str__

    def __eq__(self, other: Elve) -> bool:
        return self.pos == other.pos

    def __lt__(self, other: Elve) -> bool:
        return self.pos < other.pos


class ElvesGroup:
    def __init__(self, elves: List[Elve]) -> None:
        self.elves = elves

    def get_proposses(self):
        for elve in self.elves:
            elve.get_propos()

    def get_next_posses(self):
        for elve in self.elves:
            elve.get_next_pos()

    def get_indent_moves(self):
        intends_move = []
        for elve in self.elves:
            intends_move.append(elve.get_intends_move())
        return any(intends_move)

    def move_to_next_posses(self):
        for elve in self.elves:
            elve.move_to_next_pos()

    def take_step(self):
        self.get_proposses()
        self.get_next_posses()
        self.move_to_next_posses()

    def get_min_max(self):

        min_row, max_row, min_col, max_col = None, None, None, None

        for elve in self.elves:
            row, col = elve.pos.row, elve.pos.col
            min_row = row if min_row is None else min(min_row, row)
            max_row = row if max_row is None else max(max_row, row)
            min_col = col if min_col is None else min(min_col, col)
            max_col = col if max_col is None else max(max_col, col)

        return min_row, max_row, min_col, max_col

    def __str__(self) -> str:

        min_row, max_row, min_col, max_col = self.get_min_max()

        rows = max_row - min_row + 1
        cols = max_col - min_col + 1

        array = [["." for col in range(cols)] for row in range(rows)]

        for elve in self.elves:
            row, col = elve.pos.row - min_row, elve.pos.col - min_col
            array[row][col] = "#"

        string = "\n".join(["".join(array[row]) for row in range(rows)])

        return string + "\n"

    def empty_tiles_covered(self):

        min_row, max_row, min_col, max_col = self.get_min_max()

        return (max_row - min_row + 1) * (max_col - min_col + 1) - len(self.elves)


def get_elves(file: str) -> List[Elve]:
    elves = []
    with open("./puzzles/day_23/" + file, mode="r") as input_file:
        for row, line in enumerate(input_file.readlines()):
            for col, elm in enumerate(list(line.strip())):
                if elm == "#":
                    elves.append(Elve(Pos(row, col)))
    for elve in elves:
        other_elves = [other_elve for other_elve in elves if other_elve != elve]
        elve.other_elves = other_elves
    return elves


def part1(file: str):

    elves = get_elves(file)

    elves_group = ElvesGroup(elves)

    for i in range(10):
        elves_group.take_step()

    result = elves_group.empty_tiles_covered()

    print("Part 1:", result)


def part2(file: str):

    elves = get_elves(file)

    elves_group = ElvesGroup(elves)

    for i in range(10_000):
        if (i + 1) % 10 == 0:
            print("step", i + 1)
        elves_group.get_proposses()
        elves_group.get_next_posses()
        if elves_group.get_indent_moves():
            elves_group.move_to_next_posses()
        else:
            break

    result = i + 1

    print("Part 2:", result)


def main(file: str):
    part1(file)
    part2(file)


if __name__ == "__main__":
    main("example.txt")
