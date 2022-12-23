from __future__ import annotations

from typing import List, Union, Tuple, Literal, Optional, Dict
from pprint import pprint

from collections import namedtuple


def get_data(file: str) -> str:
    with open("./puzzles/day_22/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.replace(f"\n", "")


def get_commands_data(line: str) -> List[Union[int, str]]:

    intermediate_list = line.replace("R", ",R,").replace("L", ",L,").split(",")

    resulting_list = []

    for element in intermediate_list:
        try:
            resulting_list.append(("move", int(element)))
        except ValueError:
            resulting_list.append(("turn", element))

    return resulting_list


def get_lists_for_further_processing(file: str):

    for data in get_data(file):
        if data == "":
            pass
        elif data.startswith(" ") | data.startswith(".") | data.startswith("#"):
            yield list(data)
        else:
            yield get_commands_data(data)


def get_grove_command_data(file: str):

    uncleaned_data = []

    for element in get_lists_for_further_processing(file):
        uncleaned_data.append(element)

    commands_data = uncleaned_data.pop(-1)

    width_grove = 0

    for element in uncleaned_data:
        width_grove = max(width_grove, len(element))

    for element in uncleaned_data:
        if len(element) < width_grove:
            element += [
                " " for further_elements in range(0, width_grove - len(element))
            ]

    grove_data = uncleaned_data

    return grove_data, commands_data


def get_position_commands(file: str):

    grove_data, commands = get_grove_command_data(file)

    grove_height = len(grove_data)
    grove_width = len(grove_data[0])

    pos_dict = {}

    for y_minus_1, row in enumerate(grove_data):
        for x_minus_1, element in enumerate(row):
            x, y = x_minus_1 + 1, y_minus_1 + 1
            coords = (x, y)
            if element == "#":
                pos_dict[coords] = Position(coords, is_solid=True)
            elif element == ".":
                pos_dict[coords] = Position(coords, is_solid=False)
            else:
                pass

    ranges_by_x = dict()

    for x in range(1, grove_width + 1):
        y_min, y_max = None, None
        for y in range(1, grove_height + 1):
            x_minus_1, y_minus_1 = x - 1, y - 1
            if not (grove_data[y_minus_1][x_minus_1] == " "):
                if y_min is None:
                    y_min = y
                if y_max is None:
                    y_max = y
                else:
                    y_max = max(y, y_max)
        ranges_by_x[x] = (y_min, y_max)

    ranges_by_y = dict()

    for y in range(1, grove_height + 1):
        x_min, x_max = None, None
        for x in range(1, grove_width + 1):
            x_minus_1, y_minus_1 = x - 1, y - 1
            if not (grove_data[y_minus_1][x_minus_1] == " "):
                if x_min is None:
                    x_min = x
                if x_max is None:
                    x_max = x
                else:
                    x_max = max(x, x_max)
        ranges_by_y[y] = (x_min, x_max)

    for coords, position in pos_dict.items():

        x, y = coords

        x_min, x_max = ranges_by_y[y]
        x_right = (x + 1) if x < x_max else x_min
        x_left = (x - 1) if x > x_min else x_max

        y_min, y_max = ranges_by_x[x]
        y_down = (y + 1) if y < y_max else y_min
        y_up = (y - 1) if y > y_min else y_max

        assert x_min <= x <= x_max
        assert y_min <= y <= y_max

        position.right = pos_dict[(x_right, y)]
        position.down = pos_dict[(x, y_down)]
        position.left = pos_dict[(x_left, y)]
        position.up = pos_dict[(x, y_up)]

    y = 1
    x = ranges_by_y[1][0]

    return pos_dict[x, y], commands


class Position:
    def __init__(self, coords: Tuple[int, int], is_solid: bool = False) -> None:
        self._coords = coords
        self._is_solid = is_solid
        self._right: Optional[Position] = None
        self._down: Optional[Position] = None
        self._left: Optional[Position] = None
        self._up: Optional[Position] = None

    @property
    def coords(self):
        return self._coords

    @property
    def is_solid(self) -> bool:
        return self._is_solid

    @property
    def is_open(self) -> bool:
        return not (self._is_solid)

    # right

    @property
    def right(self) -> Position:
        if self._right is None:
            raise AttributeError
        else:
            return self._right

    @right.setter
    def right(self, pos) -> None:
        self._right = pos

    # down

    @property
    def down(self) -> Position:
        if self._down is None:
            raise AttributeError
        else:
            return self._down

    @down.setter
    def down(self, pos) -> None:
        self._down = pos

    # left

    @property
    def left(self) -> Position:
        if self._left is None:
            raise AttributeError
        else:
            return self._left

    @left.setter
    def left(self, pos) -> None:
        self._left = pos

    # up

    @property
    def up(self) -> Position:
        if self._up is None:
            raise AttributeError
        else:
            return self._up

    @up.setter
    def up(self, pos) -> None:
        self._up = pos

    def next(self, fac: int) -> Position:
        if (fac % 4) == 0:
            return self.right
        elif (fac % 4) == 1:
            return self.down
        elif (fac % 4) == 2:
            return self.left
        else:
            return self.up

    def is_next_solid(self, fac: int) -> bool:
        return self.next(fac).is_solid

    def is_next_open(self, fac: int) -> bool:
        return self.next(fac).is_open

    def __str__(self):
        return f"Position({self.coords}, {self.is_solid})"


class Person:
    def __init__(self, position: Position, facing: int = 0) -> None:
        self.position: Position = position
        self.facing = facing

    def turn_right(self) -> None:
        self.facing = (self.facing + 1) % 4

    def turn_left(self) -> None:
        self.facing = (self.facing - 1) % 4

    def turn_around(self) -> None:
        self.fac = (self.facing + 2) % 4

    def move(self) -> None:
        if self.position.is_next_open(self.facing):
            self.position = self.position.next(self.facing)


def part1(file: str) -> None:

    position, commands = get_position_commands(file)

    me = Person(position, facing=0)
    for i in range(5):
        me.move()
        print(me.position)

    for command in commands:
        if command[0] == "move":
            for move in range(command[1]):
                me.move()
        if command[0] == "turn":
            if command[1] == "R":
                me.turn_right()
            if command[1] == "L":
                me.turn_left()

    column, row = me.position.coords
    facing = me.facing

    result = 1_000 * row + 4 * column + facing

    print("Part 1:", result)


def part2(file: str) -> None:
    print(
        "Part 2:",
    )


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
