from __future__ import annotations
from typing import List, NamedTuple, Set, Tuple

from enum import Enum


def get_data(file: str) -> str:
    with open("./puzzles/day_14/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


class Position(NamedTuple):
    x: int
    y: int

    @property
    def down(self) -> Position:
        return Position(self.x, self.y + 1)

    @property
    def down_left(self) -> Position:
        return Position(self.x - 1, self.y + 1)

    @property
    def down_right(self) -> Position:
        return Position(self.x + 1, self.y + 1)


def get_rock_line_edges_list(file: str) -> List[List[List[Position]]]:

    rock_line_edges_list = []
    for data in get_data(file):
        rock_line_edges_strings = data.split(" -> ")
        rock_line_edges_string_pairs = [
            rock_line_edges_string.split(",")
            for rock_line_edges_string in rock_line_edges_strings
        ]
        rock_line_edges = [
            Position(int(rock_line_edge[0]), int(rock_line_edge[1]))
            for rock_line_edge in rock_line_edges_string_pairs
        ]
        rock_line_edges_list.append(rock_line_edges)

    return rock_line_edges_list


def make_straight_line(start: Position, stop: Position) -> List[Position]:

    line = []

    if (start.x == stop.x) & (start.y != stop.y):

        x = start.x

        if start.y < stop.y:
            for y in range(start.y, stop.y + 1):
                line.append(Position(x, y))
            return line

        else:
            for y in range(stop.y, start.y + 1):
                line.append(Position(x, y))
            return list(reversed(line))

    elif (start.x != stop.x) & (start.y == stop.y):

        y = start.y

        if start.x < stop.x:
            for x in range(start.x, stop.x + 1):
                line.append(Position(x, y))
            return line

        else:
            for x in range(stop.x, start.x + 1):
                line.append(Position(x, y))
            return list(reversed(line))

    else:
        raise AssertionError(f"Can't make line from {start} and {stop}")

    return line


def glue_lines(straight_lines: List[List[Position]]) -> List[Position]:

    glued_lines = straight_lines[0]

    for index in range(1, len(straight_lines)):

        assert glued_lines[-1] == straight_lines[index][0]
        glued_lines += straight_lines[index][1:]

    return glued_lines


def get_straight_rock_lines_list(
    rock_line_edges_list: List[List[List[Position]]],
) -> List[List[List[Position]]]:

    straight_rock_lines_list = []

    for rock_line_edges in rock_line_edges_list:

        straight_rock_lines = []

        for index in range(len(rock_line_edges) - 1):
            start = rock_line_edges[index]
            stop = rock_line_edges[index + 1]
            straight_rock_lines.append(make_straight_line(start, stop))

        straight_rock_lines_list.append(straight_rock_lines)

    return straight_rock_lines_list


def get_rock_line_list(
    straight_rock_lines_list: List[List[List[Position]]],
) -> List[List[Position]]:

    rock_line_list = []

    for straight_rock_lines in straight_rock_lines_list:
        rock_line_list.append(glue_lines(straight_rock_lines))

    return rock_line_list


def get_set_of_all_rocks(rock_line_list: List[List[Position]]) -> Set[Position]:

    all_rocks = set()

    for rock_line in rock_line_list:
        rocks = set(rock_line)
        all_rocks |= rocks

    return all_rocks


def prepare_rocks(file: str) -> Set[Position]:

    rock_line_edges_list = get_rock_line_edges_list(file)
    straight_rock_lines_list = get_straight_rock_lines_list(rock_line_edges_list)
    rock_lines_list = get_rock_line_list(straight_rock_lines_list)
    set_of_all_rocks = get_set_of_all_rocks(rock_lines_list)

    return set_of_all_rocks


class Rocks:
    def __init__(self, rocks: Set[Position]) -> None:
        self.rocks = rocks

    @property
    def shape(self) -> Tuple[int, int, int, int]:

        positions = self.rocks

        min_x = min([position.x for position in positions])
        min_y = min([position.y for position in positions])
        max_x = max([position.x for position in positions])
        max_y = max([position.y for position in positions])

        return min_x, min_y, max_x, max_y

    @property
    def abyss_starts_at(self) -> int:

        _, _, _, deepest_rock = self.shape

        return deepest_rock + 1

    def below_rocks(self, pos: Position) -> bool:
        return pos.y >= self.abyss_starts_at

    @property
    def fundament_starts_at(self) -> int:
        _, _, _, deepest_rock = self.shape
        return deepest_rock + 2

    def hits_fundament(self, pos: Position) -> bool:
        return pos.y >= self.fundament_starts_at

    def doesnt_hit_fundament(self, pos: Position) -> bool:
        return not self.hits_fundament(pos)

    def __contains__(self, pos: Position) -> bool:
        return pos in self.rocks


class RestingSand:
    def __init__(self) -> None:
        self.resting_sand = set()

    def __contains__(self, pos: Position) -> bool:
        return pos in self.resting_sand

    def add_sand(self, sand: Position) -> None:
        sand_as_set = set([sand])
        self.resting_sand = self.resting_sand | sand_as_set

    @property
    def amount(self) -> int:
        return len(self.resting_sand)


class Cave:
    def __init__(self, rocks: Rocks):
        self.rocks = rocks
        self.resting_sand = RestingSand()
        self.source_of_sand = Position(500, 0)

    @property
    def amount_of_sand(self) -> int:
        return self.resting_sand.amount

    def is_blocked(self, pos):
        is_in_rocks = pos in self.rocks
        is_in_resting_sand = pos in self.resting_sand.resting_sand
        return is_in_rocks | is_in_resting_sand

    def is_unblocked(self, pos):
        return not (self.is_blocked(pos))

    def drop_sand_until_in_abyss(self):

        possible = True

        while possible:
            falling_sand = self.source_of_sand
            falling = True
            while falling:
                if self.rocks.below_rocks(falling_sand.down):
                    falling = False
                    possible = False
                elif self.is_unblocked(falling_sand.down):
                    falling_sand = falling_sand.down
                elif self.is_unblocked(falling_sand.down_left):
                    falling_sand = falling_sand.down_left
                elif self.is_unblocked(falling_sand.down_right):
                    falling_sand = falling_sand.down_right
                else:
                    self.resting_sand.add_sand(falling_sand)
                    falling = False

    def drop_sand_until_source_blocked(self):

        while not (self.source_of_sand in self.resting_sand):
            falling_sand = self.source_of_sand
            falling = True
            while falling:
                if self.is_unblocked(
                    falling_sand.down
                ) & self.rocks.doesnt_hit_fundament(falling_sand.down):
                    falling_sand = falling_sand.down
                elif self.is_unblocked(
                    falling_sand.down_left
                ) & self.rocks.doesnt_hit_fundament(falling_sand.down_left):
                    falling_sand = falling_sand.down_left
                elif self.is_unblocked(
                    falling_sand.down_right
                ) & self.rocks.doesnt_hit_fundament(falling_sand.down_right):
                    falling_sand = falling_sand.down_right
                else:
                    self.resting_sand.add_sand(falling_sand)
                    falling = False


def part_1(file: str):

    rocks = Rocks(prepare_rocks(file))
    cave = Cave(rocks)
    cave.drop_sand_until_in_abyss()

    print("Part 1:", cave.amount_of_sand)


def part_2(file: str):

    rocks = Rocks(prepare_rocks(file))
    cave = Cave(rocks)
    cave.drop_sand_until_source_blocked()
    print("Part 2:", cave.amount_of_sand)


def main(file: str):
    part_1(file)
    part_2(file)


if __name__ == "__main__":
    main("data.txt")
