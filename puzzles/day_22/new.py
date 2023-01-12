from __future__ import annotations
from typing import Generator
from itertools import repeat


def read_data(file: str) -> Generator:
    with open(file, mode="r") as f:
        for line in f.readlines():
            yield line.replace("\n", "")


def get_raw_data(file: str) -> tuple[list[str], str]:
    raw_maze = []
    raw_directions = ""
    for line in read_data(file):
        if line == "":
            pass
        elif line[0] in [" ", ".", "#"]:
            raw_maze.append(line)
        else:
            raw_directions = line
    return raw_maze, raw_directions


def get_shape_patched_maze(raw_maze: list[str]) -> tuple[int, int, list[list[str]]]:
    height = len(raw_maze)
    width = 0
    for line in raw_maze:
        width = max(width, len(line))
    patched_maze: list[list[str]] = []
    for line in raw_maze:
        patched_line = line + " " * (len(line) - width)
        patched_maze.append(list(patched_line))
    return height, width, patched_maze


def get_tiles_size_height_width(height: int, width: int) -> tuple[int, int, int]:
    tiles_size: int = int(height / 4) if (height > width) else int(width / 4)
    tiles_height: int = 4 if (height > width) else 3
    tiles_width: int = 4 if (width > height) else 3
    return tiles_size, tiles_height, tiles_width


def get_clean_directions(raw_directions: str) -> list[tuple[str, int]]:
    intermediate_directions = (
        raw_directions.replace("R", ",R,").replace("L", ",L,").split(",")
    )
    clean_directions = []
    for direction in intermediate_directions:
        if direction == "R":
            clean_directions.append(("turn", "r"))
        elif direction == "L":
            clean_directions.append(("turn", "l"))
        else:
            clean_directions.append(("move", int(direction)))
    return clean_directions


def part2(file: str) -> None:
    raw_maze, raw_directions = get_raw_data(file)
    height, width, patched_maze = get_shape_patched_maze(raw_maze)
    tiles_size, tiles_height, tiles_width = get_tiles_size_height_width(height, width)

    tiles_range = range(0, tiles_size)
    fifty = range(0, 2)
    for i in repeat(fifty, 2):
        print(i)
    for i in repeat(fifty, 2):
        print("bla")

    directions = get_clean_directions(raw_directions)


def main() -> None:
    file = "./puzzles/day_22/example.txt"
    part2(file)


if __name__ == "__main__":
    main()
