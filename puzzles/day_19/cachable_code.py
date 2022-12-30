from __future__ import annotations

from functools import cache, lru_cache
from pprint import pprint
from typing import Tuple, FrozenSet, Dict, Literal, List, Set

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
DidntBuys = Buildables

State = Tuple[Robots, Materials]
States = FrozenSet[State]
States_Set = Set[Tuple[Robots, Materials]]


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
        material: amount + robots_dict[material]
        for material, amount in materials_dict.items()
    }

    return materials_from_dict(new_materials_dict)


@cache
def use_materials_to_make_robot(
    blueprint: BluePrint, robots: Robots, materials: Materials, robot_to_make: Robot
) -> Tuple[Robots, Materials]:

    blueprint_dict = blueprint_to_dict(blueprint)
    robots_dict = robots_to_dict(robots)
    materials_dict = materials_to_dict(materials)

    robots_result_dict: Robots_Dict = {
        robot: robots_dict[robot] + 1 if robot == robot_to_make else robots_dict[robot]
        for robot in robots_dict.keys()
    }

    materials_result_dict: Materials_Dict = {
        material: amount
        if material not in blueprint_dict[robot_to_make].keys()
        else amount - blueprint_dict[robot_to_make][material]
        for material, amount in materials_dict.items()
    }

    return robots_from_dict(robots_result_dict), materials_from_dict(
        materials_result_dict
    )


@cache
def get_buildables(blueprint: BluePrint, robots: Robots) -> Buildables:

    blueprint_dict = blueprint_to_dict(blueprint)
    robots_dict = robots_to_dict(robots)

    buildables = frozenset(
        robot
        for robot, costs in blueprint_dict.items()
        if all([robots_dict[material] != 0 for material, _ in costs.items()])
    )

    return buildables


@cache
def get_affordables(blueprint: BluePrint, materials: Materials) -> Affordables:

    blueprint_dict = blueprint_to_dict(blueprint)
    materials_dict = materials_to_dict(materials)

    affordables = frozenset(
        robot
        for robot, costs_dict in blueprint_dict.items()
        if (
            all(
                costs_dict[material] <= materials_dict[material]
                for material in costs_dict.keys()
            )
        )
    )

    return affordables


@cache
def get_states_next_minute_from_state(blueprint: BluePrint, state: State) -> States:

    next_minute_set: States_Set = set()

    robots, materials = state
    buildables = get_buildables(blueprint, robots)
    affordables = get_affordables(blueprint, materials)
    materials = make_materials(robots, materials)

    for robot in buildables:

        if robot in affordables:
            next_robots, next_materials = use_materials_to_make_robot(
                blueprint, robots, materials, robot
            )
            next_minute_set = next_minute_set.union(
                tuple([(next_robots, next_materials)])
            )
        else:
            next_minute_set = next_minute_set.union(tuple([(robots, materials)]))

    return frozenset(next_minute_set)


def get_states_next_minute(blueprint: BluePrint, states: States) -> States:
    return frozenset(
        state_next_minute
        for state in states
        for state_next_minute in get_states_next_minute_from_state(blueprint, state)
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
        robots: Robots = frozenset([("OR", 1), ("CL", 0), ("OB", 0), ("GE", 0)])
        materials: Materials = frozenset([("OR", 0), ("CL", 0), ("OB", 0), ("GE", 0)])
        states: States = frozenset([(robots, materials)])

        for time in range(1, time_left + 1):
            states = get_states_next_minute(blueprint, states)
            print(
                f"Blueprint {num} @ {str(time).zfill(2)}min has {len(states)} states..."
            )

        max_geodes = get_max_geodes_from_states(states)

        print(
            f"With blueprint {num}, you can crush up to {max_geodes} geodes in {time_left} mins, which gives a quality level of {num * max_geodes}"
        )

        get_buildables.cache_clear()
        get_affordables.cache_clear()
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
            print(
                f"Blueprint {num} @ {str(time).zfill(2)}min has {len(states)} states..."
            )

        max_geodes = get_max_geodes_from_states(states)

        print(
            f"With blueprint {num}, you can crush up to {max_geodes} geodes in {time_left} mins, which gives a quality level of {num * max_geodes}"
        )

        get_buildables.cache_clear()
        get_affordables.cache_clear()
        use_materials_to_make_robot.cache_clear()
        get_states_next_minute_from_state.cache_clear()

        result *= get_max_geodes_from_states(states)

    print("Part 2: Total quality level is", result)


def main(file: str) -> None:
    part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
