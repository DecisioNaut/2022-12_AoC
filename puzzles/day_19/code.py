from __future__ import annotations

from typing import List, Dict


def get_data(file: str):
    with open("./puzzles/day_/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


# Initial conditions
EXISTANTS: Dict[str, int] = {
    "OR": 1,
    "CL": 0,
    "OB": 0,
    "GE": 0,
}
COSTS: Dict[str, Dict[str, int]] = {
    "OR": {"OR": 4, "CL": 0, "OB": 0, "GE": 0},
    "CL": {"OR": 2, "CL": 0, "OB": 0, "GE": 0},
    "OB": {"OR": 3, "CL": 14, "OB": 0, "GE": 0},
    "GE": {"OR": 2, "CL": 0, "OB": 7, "GE": 0},
}
YIELDS = {
    "OR": 0,
    "CL": 0,
    "OB": 0,
    "GE": 0,
}

BUILDABLE: Dict[str, bool] = {
    THIS_ROBOT: all(
        [EXISTANTS[ROBOT] != 0 for ROBOT, COSTS in THIS_COSTS.items() if COSTS != 0]
    )
    for THIS_ROBOT, THIS_COSTS in COSTS.items()
}
AFFORDABLE: Dict[str, bool] = {
    THIS_ROBOT: all([YIELDS[ROBOT] >= COSTS for ROBOT, COSTS in THIS_COSTS.items()])
    for THIS_ROBOT, THIS_COSTS in COSTS.items()
}


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
