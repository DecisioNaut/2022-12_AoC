from __future__ import annotations

from functools import partial, cache
from pprint import pprint
from typing import Tuple, FrozenSet, Callable, Dict, Literal, Union

Robot = Literal["OR", "CL", "OB", "GE"]
Robots = FrozenSet[Tuple[Robot, int]]
Robots_Dict = Dict[Robot, int]

Material = Robot
Materials = Robots
Materials_Dict = Robots_Dict

Costs = Robots
Costs_Dict = Robots_Dict

BluePrint = FrozenSet[Tuple[Robot, Costs]]
BluePrint_Dict = Dict[Robot, Costs_Dict]

BluePrints = FrozenSet[Tuple[int, BluePrint]]
BluePrints_Dict = Dict[int, BluePrint_Dict]

Buildables = FrozenSet[Robot]
Affordables = Buildables


@cache
def robots_to_dict(robots: Robots) -> Robots_Dict:
    return {robot: num for robot, num in robots}


def robots_from_dict(robots_dict: Robots_Dict) -> Robots:
    return frozenset((robot, num) for robot, num in robots_dict.items())


@cache
def materials_to_dict(materials: Materials) -> Materials_Dict:
    return {material: amount for material, amount in materials}


def materials_from_dict(materials_dict: Materials_Dict) -> Materials:
    return frozenset((material, amount) for material, amount in materials_dict.items())


@cache
def costs_to_dict(costs: Costs) -> Costs_Dict:
    return {material: cost for material, cost in costs}


def costs_from_dict(costs_dict: Costs_Dict) -> Costs:
    return frozenset((material, cost) for material, cost in costs_dict.items())


@cache
def blueprint_to_dict(blueprint: BluePrint) -> BluePrint_Dict:
    return dict((robot, costs_to_dict(costs)) for robot, costs in blueprint)


def blueprint_from_dict(blueprint_dict: BluePrint_Dict) -> BluePrint:
    return frozenset(
        (robot, costs_from_dict(costs)) for robot, costs in blueprint_dict.items()
    )


def get_data(file: str):
    with open("./puzzles/day_19/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def get_blueprints(file: str) -> BluePrints:

    nums, blueprints = [], []

    for num, data in enumerate(get_data(file), 1):

        robots_costs_array = (
            data.split(":")[1]
            .replace("Each ", "")
            .replace(" robot costs ", ":")
            .replace(" and ", ",")
            .replace(" ore", " OR")
            .replace(" clay", " CL")
            .replace(" obsidian", " OB")
            .replace(" geode", " GE")[0:-1]
            .split(".")
        )

        robots, robots_costs = [], []

        for robot_costs in robots_costs_array:

            robot_costs = robot_costs.strip()
            robot, costs = robot_costs.split(":")
            costs = costs.split(",")

            materials, amounts = [], []

            for cost in costs:
                amount_str, material = cost.split(" ")
                amount = int(amount_str)
                materials.append(material)
                amounts.append(amount)

            robot_costs_fs = frozenset(zip(materials, amounts))

            robots.append(robot)
            robots_costs.append(robot_costs_fs)

        blueprint = frozenset(zip(robots, robots_costs))

        nums.append(num)
        blueprints.append(blueprint)

    blueprints_fs = frozenset(zip(nums, blueprints))

    return blueprints_fs


@cache
def get_crushed_geodes(materials: Materials) -> int:
    return [material for material in materials if material[0] == "GE"][0][1]


@cache
def make_materials(robots: Robots, materials: Materials) -> Materials:

    robots_dict = robots_to_dict(robots)
    materials_dict = materials_to_dict(materials)

    new_materials_dict: Materials_Dict = {
        material: (amount + robots_dict[material])
        for material, amount in materials_dict.items()
    }

    return materials_from_dict(new_materials_dict)


@cache
def get_buildables(blueprint: BluePrint, robots: Robots) -> Buildables:

    blueprint_dict = blueprint_to_dict(blueprint)
    robots_dict = robots_to_dict(robots)

    return frozenset(
        [
            robot
            for robot, costs in blueprint_dict.items()
            if all([robots_dict[material] != 0 for material, _ in costs.items()])
        ]
    )


@cache
def get_affordables(
    blueprint: BluePrint, materials: Materials, buildables: Buildables
) -> Affordables:

    blueprint_dict = blueprint_to_dict(blueprint)
    materials_dict = materials_to_dict(materials)

    return frozenset(
        [
            robot
            for robot in buildables
            if all(
                [
                    materials_dict[material] >= blueprint_dict[robot][material]
                    for material in blueprint_dict[robot].keys()
                ]
            )
        ]
    )


@cache
def use_materials_to_make_robot(
    blueprint: BluePrint, robots: Robots, materials: Materials, robot: Robot
) -> Tuple[Robots, Materials]:

    blueprint_dict = blueprint_to_dict(blueprint)
    robots_dict = robots_to_dict(robots)
    materials_dict = materials_to_dict(materials)

    robots_result_dict: Robots_Dict = {
        robot_: robots_dict[robot_] + 1 if robot_ == robot else robots_dict[robot_]
        for robot_ in robots_dict.keys()
    }

    materials_result_dict: Materials_Dict = {
        material: amount
        if material not in blueprint_dict[robot].keys()
        else amount - blueprint_dict[robot][material]
        for material, amount in materials_dict.items()
    }

    return robots_from_dict(robots_result_dict), materials_from_dict(
        materials_result_dict
    )


@cache
def get_max_crushed_geodes(
    blueprint: BluePrint, robots: Robots, materials: Materials, time_left
) -> int:

    max_crushed_geodes = get_crushed_geodes(materials)

    buildables = get_buildables(blueprint, robots)

    for robot in buildables:
        crushed_geodes = 0
        robots_ = robots
        materials_ = materials
        for time in range(time_left - 1, -1, -1):
            affordables = get_affordables(blueprint, materials_, buildables)
            materials_ = make_materials(robots_, materials_)
            if robot in affordables:
                robots_, materials_ = use_materials_to_make_robot(
                    blueprint, robots_, materials_, robot
                )
                crushed_geodes = get_max_crushed_geodes(
                    blueprint, robots_, materials_, time
                )
                break
        max_crushed_geodes = max(crushed_geodes, max_crushed_geodes)

    return max_crushed_geodes


def part1(file: str) -> None:

    blueprints = get_blueprints(file)
    result = 0

    for num, blueprint in sorted(blueprints):

        robots = frozenset([("OR", 1), ("CL", 0), ("OB", 0), ("GE", 0)])
        materials = frozenset([("OR", 0), ("CL", 0), ("OB", 0), ("GE", 0)])
        max_crushed_geodes = get_max_crushed_geodes(blueprint, robots, materials, 24)

        print(
            f"With blueprint {num}, you can crush up to {max_crushed_geodes} geodes, which gives a quality level of {num * max_crushed_geodes}"
        )

        result += num * max_crushed_geodes

    print("Part 1: Total quality level is", result)


def part2(file: str) -> None:
    ...


def main(file: str) -> None:
    part1(file)
    part2(file)


if __name__ == "__main__":
    main("example.txt")


""" Robots = Dict[str, int]
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
    unsorted_buildables = [
        robot
        for robot, costs in blueprint.items()
        if all([robots[material] != 0 for material, cost in costs.items()])
    ]
    sorted_buildables = [
        robot for robot in ["GE", "OB", "CL", "OR"] if robot in unsorted_buildables
    ]

    return sorted_buildables


Affordables = List[str]


def general_get_affordables(
    blueprint: BluePrint, materials: Materials, buildables: Buildables
) -> Affordables:
    return [
        robot
        for robot in buildables
        if all(
            [
                materials[material] >= blueprint[robot][material]
                for material in blueprint[robot].keys()
            ]
        )
    ]


def general_use_materials_to_make_robot(
    blueprint: BluePrint, robots: Robots, materials: Materials, robot: str
) -> Tuple[Robots, Materials]:

    robots_result = {
        robot_: robots[robot_] + 1 if robot_ == robot else robots[robot_]
        for robot_ in ["OR", "CL", "OB", "GE"]
    }

    materials_result = {
        material: amount
        if material not in blueprint[robot].keys()
        else amount - blueprint[robot][material]
        for material, amount in materials.items()
    }

    return robots_result, materials_result


def get_max_crushed_geodes_fun(
    blueprint: BluePrint,
) -> Callable[[Robots, Materials, int], int]:

    get_buildables = partial(general_get_buildables, blueprint)
    get_affordables = partial(general_get_affordables, blueprint)
    use_materials_to_make_robot = partial(
        general_use_materials_to_make_robot, blueprint
    )

    def get_max_crushed_geodes(robots: Robots, materials: Materials, time_left) -> int:

        max_crushed_geodes = get_crushed_geodes(materials)

        buildables = get_buildables(robots)

        for robot in buildables:
            crushed_geodes = 0
            robots_ = robots
            materials_ = materials
            for time in range(time_left - 1, -1, -1):
                affordables = get_affordables(materials_, buildables)
                materials_ = make_materials(robots_, materials_)
                if robot in affordables:
                    robots_, materials_ = use_materials_to_make_robot(
                        robots_, materials_, robot
                    )
                    crushed_geodes = get_max_crushed_geodes(
                        robots_, materials_, time_left=time
                    )
                    break
            max_crushed_geodes = max(crushed_geodes, max_crushed_geodes)

        return max_crushed_geodes

    return get_max_crushed_geodes


BluePrints = Dict[int, BluePrint]


def get_blueprints(file: str) -> BluePrints:

    blueprints: BluePrints = dict()

    for num, data in enumerate(get_data(file), 1):
        robots_costs_array = (
            data.split(":")[1]
            .replace("Each ", "")
            .replace(" robot costs ", ":")
            .replace(" and ", ",")
            .replace(" ore", " OR")
            .replace(" clay", " CL")
            .replace(" obsidian", " OB")
            .replace(" geode", " GE")[0:-1]
            .split(".")
        )
        robot_costs_dict = dict()
        for robot_costs in robots_costs_array:
            robot_costs = robot_costs.strip()
            robot, costs = robot_costs.split(":")
            costs = costs.split(",")
            cost_dict = dict()
            for cost in costs:
                amount_str, material = cost.split(" ")
                amount = int(amount_str)
                cost_dict[material] = amount
            robot_costs_dict[robot] = cost_dict
        blueprints[num] = robot_costs_dict
    return blueprints


def part1(file: str) -> None:

    blueprints = get_blueprints(file)
    result = 0

    for num, blueprint in blueprints.items():

        robots = {"OR": 1, "CL": 0, "OB": 0, "GE": 0}
        materials = {"OR": 0, "CL": 0, "OB": 0, "GE": 0}

        get_max_crushed_geodes = get_max_crushed_geodes_fun(blueprint)
        max_crushed_geodes = get_max_crushed_geodes(robots, materials, 24)

        print(
            f"With blueprint {num}, you can crush up to {max_crushed_geodes} geodes, which gives a quality level of {num * max_crushed_geodes}"
        )

        result += num * max_crushed_geodes

    print("Part 1: Total quality level is", result)


def part2(file: str) -> None:

    blueprints = get_blueprints(file)
    result = 1

    for num, blueprint in blueprints.items():

        if num <= 3:

            robots = {"OR": 1, "CL": 0, "OB": 0, "GE": 0}
            materials = {"OR": 0, "CL": 0, "OB": 0, "GE": 0}

            get_max_crushed_geodes = get_max_crushed_geodes_fun(blueprint)
            max_crushed_geodes = get_max_crushed_geodes(robots, materials, 32)

            print(
                f"With blueprint {num}, you can crush up to {max_crushed_geodes} geodes in 32mins, which gives a quality level of {num * max_crushed_geodes}"
            )

            result *= max_crushed_geodes

    print("Part 2: Quality level product is", result)


def main(file: str) -> None:

    # part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
 """
