from __future__ import annotations

from typing import List
from abc import ABC, abstractmethod


def get_data(file: str):
    with open("./puzzles/day_/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


class Robot:
    def __init__(
        self,
        ore_costs: int | None = None,
        clay_costs: int | None = None,
        obsedian_costs: int | None = None,
        ore_pm: int = 0,
        clay_pm: int = 0,
        obsidian_pm: int = 0,
        geodes_pm: int = 0,
    ) -> None:
        self._ore_costs = ore_costs
        self._clay_costs = clay_costs
        self._obsidian_costs = obsedian_costs
        self._ore_pm = ore_pm
        self._clay_pm = clay_pm
        self._obsedian_pm = obsidian_pm
        self._geodes_pm = geodes_pm


class BluePrint:
    ...


def part1(file: str) -> None:
    data = get_data(file)
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
