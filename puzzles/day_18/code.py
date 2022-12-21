from __future__ import annotations

from typing import Tuple, List
from enum import Enum
from pprint import pprint


def get_data(file: str) -> str:
    with open("./puzzles/day_18/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def get_coord(file: str) -> Tuple[int, int, int]:
    for data in get_data(file):
        yield tuple([int(element) for element in data.split(",")])


def get_coords(file: str) -> List[Tuple[int, int, int]]:
    return [coord for coord in get_coord(file)]


def part1(file: str) -> None:

    coords = get_coords(file)

    uncovered_sides = 0

    for coord in coords:

        x, y, z = coord

        adjacent_coords = [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ]

        for adjacent_coord in adjacent_coords:

            try:
                coords.index((adjacent_coord))

            except ValueError:
                uncovered_sides += 1

            except Exception as e:
                raise Exception

    print("Part 1:", uncovered_sides)


def part2(file: str) -> None:

    xmax, ymax, zmax = 0, 0, 0

    lava_coords = []

    # Find minimum, maximum of xs, ys and zs
    # And create list of lava coords

    lava_coords = []

    for counter, coord in enumerate(get_coord(file)):
        if counter == 0:
            xmin, ymin, zmin = coord
            xmax, ymax, zmax = coord
        else:
            x, y, z = coord
            xmin, ymin, zmin = min(xmin, x), min(ymin, y), min(zmin, z)
            xmax, ymax, zmax = max(xmax, x), max(ymax, y), max(zmax, z)

        lava_coords.append(coord)

    # Create types of material

    # Create cave leaving start and end empty of lava

    cave = [
        [
            [" " for z in range(-zmin, zmax - zmin + 3)]
            for y in range(-ymin, ymax - ymin + 3)
        ]
        for x in range(-xmin, xmax - xmin + 3)
    ]

    # Set cave to lava where applicable

    for lava_coord in lava_coords:
        x, y, z = lava_coord
        cave[x + 1][y + 1][z + 1] = "*"

    # Set very first cave element to water

    cave[0][0][0] = "~"
    coords_to_investigate = [(0, 0, 0)]
    lava_surface_size = 0

    # Iterate throught the outside of the lava

    while coords_to_investigate != []:

        current_coord = coords_to_investigate.pop(0)

        x, y, z = current_coord

        adjacent_coords = [
            (max(x - 1, 0), y, z),
            (min(x + 1, xmax + 2), y, z),
            (x, max(y - 1, 0), z),
            (x, min(y + 1, ymax + 2), z),
            (x, y, max(z - 1, 0)),
            (x, y, min(z + 1, zmax + 2)),
        ]

        adjacent_coords = set(
            [
                adjacent_coord
                for adjacent_coord in adjacent_coords
                if adjacent_coord != current_coord
            ]
        )

        for adjacent_coord in adjacent_coords:

            x_adj, y_adj, z_adj = adjacent_coord
            adj_material = cave[x_adj][y_adj][z_adj]

            if adj_material == "*":
                lava_surface_size += 1
            elif adj_material == " ":
                coords_to_investigate.append(adjacent_coord)
                cave[x_adj][y_adj][z_adj] = "~"
            elif adj_material == "~":
                pass

    print("Part 2:", lava_surface_size)


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
