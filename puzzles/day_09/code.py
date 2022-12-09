from __future__ import annotations

from typing import Literal, List
from pprint import pprint


def get_data(file: str):
    with open("./puzzles/day_09/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip().split(" ")


class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Vector) -> bool:
        return (self.x == other.x) & (self.y == other.y)

    def __add__(self, other: Vector) -> Vector:
        assert isinstance(other, Vector)
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other: Vector) -> Vector:
        assert isinstance(other, Vector)
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    @property
    def pull(self) -> Vector:
        if (abs(self.x) <= 1) & (abs(self.y) <= 1):
            return Vector(0, 0)
        # elif (abs(self.x) >= 2) & (abs(self.y) >= 2):
        #    return AssertionError
        else:

            def create_pull(x_or_y: int) -> int:
                if x_or_y == 0:
                    return 0
                elif x_or_y >= 1:
                    return 1
                elif x_or_y <= -1:
                    return -1

            pull_x = create_pull(self.x)
            pull_y = create_pull(self.y)
            return Vector(pull_x, pull_y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    __repr__ = __str__


class MovingPart:
    def __init__(self, x_start: int, y_start: int) -> None:
        start_position = Vector(x_start, y_start)
        self.position = start_position
        self.history = [start_position]

    def move_by_instruction(self, direction: Literal["R", "U", "D", "R"]) -> None:
        match direction:
            case "R":
                move = Vector(1, 0)
            case "U":
                move = Vector(0, 1)
            case "D":
                move = Vector(0, -1)
            case "L":
                move = Vector(-1, 0)
            case _:
                raise ValueError
        new_position = self.position + move
        self.position = new_position
        self.history.append(new_position)

    def follow_by_position(self, pulling_position: Vector) -> None:
        difference = pulling_position - self.position
        pull = difference.pull
        new_position = self.position + pull
        self.position = new_position
        self.history.append(new_position)

    @property
    def visited_positions_count(self):
        visited_positions = []
        for position in self.history:
            if not (position in visited_positions):
                visited_positions.append(position)
        return len(visited_positions)


def part_1():
    directions = []
    for data in get_data("data.txt"):
        directions.append({"instruction": data[0], "repeat": int(data[1])})

    head = MovingPart(0, 0)
    tail = MovingPart(0, 0)

    for direction in directions:
        for i in range(direction["repeat"]):
            head.move_by_instruction(direction["instruction"])
            tail.follow_by_position(head.position)

    print("Part 1:", tail.visited_positions_count)


def part_2():
    directions = []
    for data in get_data("data.txt"):
        directions.append({"instruction": data[0], "repeat": int(data[1])})

    head = MovingPart(0, 0)
    knot_1 = MovingPart(0, 0)
    knot_2 = MovingPart(0, 0)
    knot_3 = MovingPart(0, 0)
    knot_4 = MovingPart(0, 0)
    knot_5 = MovingPart(0, 0)
    knot_6 = MovingPart(0, 0)
    knot_7 = MovingPart(0, 0)
    knot_8 = MovingPart(0, 0)
    tail = MovingPart(0, 0)

    for direction in directions:
        for i in range(direction["repeat"]):
            head.move_by_instruction(direction["instruction"])
            knot_1.follow_by_position(head.position)
            knot_2.follow_by_position(knot_1.position)
            knot_3.follow_by_position(knot_2.position)
            knot_4.follow_by_position(knot_3.position)
            knot_5.follow_by_position(knot_4.position)
            knot_6.follow_by_position(knot_5.position)
            knot_7.follow_by_position(knot_6.position)
            knot_8.follow_by_position(knot_7.position)
            tail.follow_by_position(knot_8.position)

    print("Part 2:", tail.visited_positions_count)


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
