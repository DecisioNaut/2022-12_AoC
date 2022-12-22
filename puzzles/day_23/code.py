from __future__ import annotations

from typing import List


def get_data(file: str):
    with open("./puzzles/day_23/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def part1(file: str) -> None:
    print(
        "Part 1:",
    )


def part2(file: str) -> None:
    data = get_data(file)
    print(
        "Part 2:",
    )


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("example.txt")
