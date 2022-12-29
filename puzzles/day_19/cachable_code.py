from __future__ import annotations

from functools import cache
from pprint import pprint
from typing import Tuple, FrozenSet, Dict, Literal, List

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

State = Tuple[Robots, Materials]
States = FrozenSet[State]


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
def get_states_next_minute_from_state(blueprint: BluePrint, state: State) -> States:

    next_robots_list: List[Robots] = []
    next_materials_list: List[Materials] = []

    robots, materials = state

    buildables = get_buildables(blueprint, robots)
    affordables = get_affordables(blueprint, materials, buildables)
    intermediate_materials = make_materials(robots, materials)

    if affordables:
        for affordable in affordables:
            next_robots, next_materials = use_materials_to_make_robot(
                blueprint, robots, intermediate_materials, affordable
            )
            next_robots_list.append(next_robots)
            next_materials_list.append(next_materials)
    else:
        next_robots_list.append(robots)
        next_materials_list.append(intermediate_materials)

    return frozenset(zip(next_robots_list, next_materials_list))


def get_states_next_minute(blueprint: BluePrint, states: States) -> States:
    return frozenset(
        [
            state_next_minute
            for state in states
            for state_next_minute in get_states_next_minute_from_state(blueprint, state)
        ]
    )


def get_max_geodes_from_states(states: States) -> int:

    max_geodes = 0

    for state in states:
        _, materials = state
        for material, amount in materials:
            if material == "GE":
                max_geodes = max(amount, max_geodes)

    return max_geodes


def part1(file: str) -> None:

    blueprints = get_blueprints(file)
    result = 0

    for num, blueprint in sorted(blueprints):

        time_left = 24
        robots = frozenset([("OR", 1), ("CL", 0), ("OB", 0), ("GE", 0)])
        materials = frozenset([("OR", 0), ("CL", 0), ("OB", 0), ("GE", 0)])
        states = frozenset([(robots, materials)])

        for time in range(1, time_left + 1):
            states = get_states_next_minute(blueprint, states)

        get_affordables.cache_clear()
        get_buildables.cache_clear()
        use_materials_to_make_robot.cache_clear()
        get_states_next_minute_from_state.cache_clear()

        result += num * get_max_geodes_from_states(states)

    print("Part 1: Total quality level is", result)


def part2(file: str) -> None:

    blueprints = get_blueprints(file)
    result = 1

    for num, blueprint in sorted(blueprints):

        if num > 3:
            break

        time_left = 32
        robots = frozenset([("OR", 1), ("CL", 0), ("OB", 0), ("GE", 0)])
        materials = frozenset([("OR", 0), ("CL", 0), ("OB", 0), ("GE", 0)])
        states = frozenset([(robots, materials)])

        for time in range(1, time_left + 1):
            states = get_states_next_minute(blueprint, states)
            print(num, time, len(states))

        get_affordables.cache_clear()
        get_buildables.cache_clear()
        use_materials_to_make_robot.cache_clear()
        get_states_next_minute_from_state.cache_clear()

        result *= get_max_geodes_from_states(states)

    print("Part 2: Total quality level is", result)


def main(file: str) -> None:
    # part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
