from __future__ import annotations

from functools import cache
from itertools import cycle
from typing import Tuple, Literal, List

Jet = Literal["<", ">"]
JetPattern = Tuple[Jet, ...]

X, Y = int, int
Point = Tuple[X, Y]
Shape = Tuple[Point, ...]
ShapePattern = Tuple[Shape, ...]

Base = Shape


def get_base() -> Base:
    base = ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0))
    return base


@cache
def calibrate_base(base: Base) -> Tuple[Base, Y]:

    y_calibration = max(y for _, y in base)
    next_base = tuple((x, y - y_calibration) for x, y in base)

    return next_base, y_calibration


@cache
def simplify_base(base: Base) -> Base:

    y_max = max(
        y for _, y in base if all((x, y) in base for x in [1, 2, 3, 4, 5, 6, 7])
    )
    # y_max_7 = max(y for x, y in base if (x == 7))
    # y_min = min(y_max_1, y_max_7)
    simplified_base = tuple((x, y) for x, y in base if y >= y_max)

    return simplified_base


def get_shape_pattern() -> ShapePattern:

    shape_1: Shape = ((3, 4), (4, 4), (5, 4), (6, 4))
    shape_2: Shape = ((4, 4), (3, 5), (4, 5), (5, 5), (4, 6))
    shape_3: Shape = ((3, 4), (4, 4), (5, 4), (5, 5), (5, 6))
    shape_4: Shape = ((3, 4), (3, 5), (3, 6), (3, 7))
    shape_5: Shape = ((3, 4), (4, 4), (3, 5), (4, 5))

    shape_pattern: ShapePattern = (shape_1, shape_2, shape_3, shape_4, shape_5)

    return shape_pattern


@cache
def get_next_shape(shape_pattern: ShapePattern) -> Tuple[Shape, ShapePattern]:

    next_shape = shape_pattern[0]
    next_shape_pattern = shape_pattern[1:] + (next_shape,)

    return next_shape, next_shape_pattern


def get_jet_pattern(file: str) -> JetPattern:

    jet_pattern: JetPattern = tuple()
    jets: List[Jet] = ["<", ">"]

    with open("./puzzles/day_17/" + file, mode="r") as f:
        for line in f.readlines():
            for char in line:
                if char in jets:
                    jet_pattern += (char,)

    return jet_pattern


@cache
def get_next_jet(jet_pattern: JetPattern) -> Tuple[Jet, JetPattern]:

    next_jet = jet_pattern[0]
    next_jet_pattern = jet_pattern[1:] + (next_jet,)

    return next_jet, next_jet_pattern


def move_right_if_possible(shape: Shape, base: Base) -> Shape:

    potential_new_shape = tuple((x + 1, y) for x, y in shape)

    if any(x == 8 for x, _ in potential_new_shape) | any(
        point in base for point in potential_new_shape
    ):
        return shape
    else:
        return potential_new_shape


def move_left_if_possible(shape: Shape, base: Base) -> Shape:

    potential_new_shape = tuple((x - 1, y) for x, y in shape)

    if any(x == 0 for x, _ in potential_new_shape) | any(
        point in base for point in potential_new_shape
    ):
        return shape
    else:
        return potential_new_shape


def move_down_if_possible(shape: Shape, base: Base) -> Tuple[Shape, Base]:

    potential_new_shape = tuple((x, y - 1) for x, y in shape)

    if any(point in base for point in potential_new_shape):
        return (), base + shape
    else:
        return potential_new_shape, base


def part1(file: str) -> None:

    # Basic setup
    height = 0
    base = get_base()
    shape_pattern = get_shape_pattern()
    jet_pattern = get_jet_pattern(file)

    # Cycle through patterns
    rocks_shapes = enumerate(cycle(shape_pattern), 1)
    jets = cycle(jet_pattern)

    # Set rock counter
    rocks = 0

    while rocks < 2022:

        rocks, shape = next(rocks_shapes)

        while shape:

            jet = next(jets)

            if jet == ">":
                shape = move_right_if_possible(shape, base)
            elif jet == "<":
                shape = move_left_if_possible(shape, base)
            shape, base = move_down_if_possible(shape, base)

        base, y_calibration = calibrate_base(base)
        height += y_calibration
        base = simplify_base(base)

    print(height)


def part2(file: str) -> None:

    height = 0
    base = get_base()
    shape_pattern = get_shape_pattern()
    jet_pattern = get_jet_pattern(file)

    base_shape_pat_jet_pat_cache = []
    height_cache = []

    while (base, shape_pattern, jet_pattern) not in base_shape_pat_jet_pat_cache:

        base_shape_pat_jet_pat_cache.append((base, shape_pattern, jet_pattern))
        height_cache.append(height)

        shape, shape_pattern = get_next_shape(shape_pattern)

        while shape:

            jet, jet_pattern = get_next_jet(jet_pattern)

            if jet == ">":
                shape = move_right_if_possible(shape, base)
            elif jet == "<":
                shape = move_left_if_possible(shape, base)
            shape, base = move_down_if_possible(shape, base)

            if shape:
                y_min_shape = min(y for _, y in shape)
                y_min_base = min(y for _, y in base)
                assert y_min_base < y_min_shape

        base, y_calibration = calibrate_base(base)
        height += y_calibration
        base = simplify_base(base)

    len_cache = (
        len(height_cache)
        if len(height_cache) == len(base_shape_pat_jet_pat_cache)
        else AssertionError
    )
    index_of_first_double_entry = base_shape_pat_jet_pat_cache.index(
        (base, shape_pattern, jet_pattern)
    )
    height_at_first_double_entry = height_cache[index_of_first_double_entry]

    print("Length of cache:              ", len_cache)
    print("Index of first double entry:  ", index_of_first_double_entry)
    print()

    print("Current height:               ", height)
    print("Height at first double entry: ", height_at_first_double_entry)
    print()


def main(file: str) -> None:
    # part1(file)
    part2(file)


if __name__ == "__main__":
    file = "example.txt"
    main(file)
