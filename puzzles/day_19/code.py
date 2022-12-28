from __future__ import annotations

from functools import partial
from typing import List, Dict, Tuple
from copy import deepcopy


def get_data(file: str):
    with open("./puzzles/day_/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


Robots = Dict[str, int]
Materials = Dict[str, int]


def get_crushed_geodes(materials: Materials) -> int:
    return materials["GE"]


def make_materials(robots: Robots, materials: Materials) -> Materials:
    return {
        robot: robots[robot] + materials[robot] for robot in ["OR", "CL", "OB", "GE"]
    }


BluePrint = Dict[str, Dict[str, int]]
Buildables = List[str]


def general_get_buildables(blueprint: BluePrint, robots: Robots) -> Buildables:
    return [
        robot
        for robot, costs in blueprint.items()
        if all([robots[robot_] != 0 for robot_, cost in costs.items() if cost != 0])
    ]


Affordables = Dict[str, bool]


def general_get_affordables(blueprint: BluePrint, materials: Materials) -> Affordables:
    return [
        robot
        for robot in ["OR", "CL", "OB", "GE"]
        if all(
            [
                materials[robot_] >= blueprint[robot][robot_]
                for robot_ in ["OR", "CL", "OB", "GE"]
            ]
        )
    ]


def general_use_materials_to_make_robot(
    blueprint: BluePrint, robots: Robots, materials: Materials, robot: str
) -> Tuple[Robots, Materials]:

    costs = blueprint[robot]

    materials_result = {
        material: amount - costs[material] for material, amount in materials.items()
    }

    robots_result = {
        robot_: robots[robot_] + 1 if robot_ == robot else robots[robot_]
        for robot_ in ["OR", "CL", "OB", "GE"]
    }

    return robots_result, materials_result


def general_get_max_crushed_geodes(
    blueprint: BluePrint, robots: Robots, materials: Materials, time_left: int = 24
) -> int:

    max_crushed_geodes = get_crushed_geodes(materials)

    buildables = general_get_buildables(blueprint, robots)

    for robot in buildables:
        crushed_geodes = 0
        robots_ = deepcopy(robots)
        materials_ = deepcopy(materials)
        time_left_ = time_left
        for time in range(time_left_ - 1, -1, -1):
            affordables = general_get_affordables(blueprint, materials_)
            materials_ = make_materials(robots_, materials_)
            if robot in affordables:
                robots_, materials_ = general_use_materials_to_make_robot(
                    blueprint, robots_, materials_, robot
                )
                crushed_geodes = general_get_max_crushed_geodes(
                    blueprint, robots_, materials_, time_left=time
                )
                break
        max_crushed_geodes = max(crushed_geodes, max_crushed_geodes)

    return max_crushed_geodes


def part1(file: str) -> None:

    robots = {"OR": 1, "CL": 0, "OB": 0, "GE": 0}
    materials = {"OR": 0, "CL": 0, "OB": 0, "GE": 0}

    blueprint = {
        "OR": {"OR": 4, "CL": 0, "OB": 0, "GE": 0},
        "CL": {"OR": 2, "CL": 0, "OB": 0, "GE": 0},
        "OB": {"OR": 3, "CL": 14, "OB": 0, "GE": 0},
        "GE": {"OR": 2, "CL": 0, "OB": 7, "GE": 0},
    }

    print(general_get_max_crushed_geodes(blueprint, robots, materials, time_left=24))


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
