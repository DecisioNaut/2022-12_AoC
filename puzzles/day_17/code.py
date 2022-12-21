from __future__ import annotations

from typing import List, Tuple, Any, Literal, Generator
from itertools import cycle


def get_data(file: str):
    with open("./puzzles/day_17/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


class Shape:
    def __init__(self, shape_pattern: List[Tuple[int, int]], height: int) -> None:
        self._positions: List[Tuple[int, int]] = [
            (x, y + height) for x, y in shape_pattern
        ]
        self._active = True

    @property
    def positions(self):
        return self._positions

    @property
    def down(self) -> List[Tuple[int, int]]:
        return [(x, y - 1) for x, y in self._positions]

    def move_down(self):
        self._positions = [(x, y - 1) for x, y in self._positions]

    @property
    def right(self) -> List[Tuple[int, int]]:
        return [(x + 1, y) for x, y in self._positions]

    def move_right(self):
        self._positions = [(x + 1, y) for x, y in self._positions]

    @property
    def left(self) -> List[Tuple[int, int]]:
        return [(x - 1, y) for x, y in self._positions]

    def move_left(self):
        self._positions = [(x - 1, y) for x, y in self._positions]

    def destroy(self) -> None:
        self._active = False

    def __bool__(self):
        return self._active


class Chamber:
    def __init__(
        self,
        shapes_patterns: List[List[Tuple[int, int]]],
        wind_pattern: List[Literal["<", ">"]],
        width: int = 7,
    ):
        self._shapes_patterns: Generator[List[Tuple[int, int]]] = cycle(shapes_patterns)
        self._wind_pattern: Generator[Literal["<", ">"]] = cycle((wind_pattern))
        self._width: int = width
        self._landed_shapes: List[Tuple[int, int]] = [
            (i, 0) for i in range(self._width + 2)
        ]  # Start with floor

    @property
    def height(self):
        return max([y for x, y in self._landed_shapes])

    def hits_walls(self, shape_positions: List[Tuple[int, int]]) -> bool:
        for shape_position in shape_positions:
            x, y = shape_position
            if (x == 0) | (x == self._width + 1):
                return True
        return False

    def hits_landed_shapes(self, shape_positions: List[Tuple[int, int]]) -> bool:
        for shape_position in shape_positions:
            if shape_position in self._landed_shapes:
                return True
        return False

    def hits_something(self, shape_positions: List[Tuple[int, int]]) -> bool:
        return self.hits_walls(shape_positions) | self.hits_landed_shapes(
            shape_positions
        )

    def fill(self, num_shapes: int):

        for counter, shape_pattern in enumerate(self._shapes_patterns):

            if counter == num_shapes:
                break

            current_height = self.height
            shape = Shape(shape_pattern, current_height + 3)

            while shape:

                for wind in self._wind_pattern:

                    if wind == ">":
                        if not (self.hits_something(shape.right)):
                            shape.move_right()
                    elif wind == "<":
                        if not (self.hits_something(shape.left)):
                            shape.move_left()
                    else:
                        raise ValueError

                    if not (self.hits_something(shape.down)):
                        shape.move_down()
                    else:
                        self._landed_shapes += shape.positions
                        shape.destroy()
                        break


def part1(file: str) -> None:

    shape_pattern_1 = [(3, 1), (4, 1), (5, 1), (6, 1)]
    shape_pattern_2 = [(4, 1), (3, 2), (4, 2), (5, 2), (4, 3)]
    shape_pattern_3 = [(3, 1), (4, 1), (5, 1), (5, 2), (5, 3)]
    shape_pattern_4 = [(3, 1), (3, 2), (3, 3), (3, 4)]
    shape_pattern_5 = [(3, 1), (4, 1), (3, 2), (4, 2)]

    shape_patterns = [
        shape_pattern_1,
        shape_pattern_2,
        shape_pattern_3,
        shape_pattern_4,
        shape_pattern_5,
    ]

    for data in get_data(file):
        wind_pattern = list(data)

    chamber = Chamber(shape_patterns, wind_pattern)

    chamber.fill(2022)

    print("Part 1:", chamber.height)


def part2(file: str) -> None:
    data = get_data(file)
    print(
        "Part 2:",
    )


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
