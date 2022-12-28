from __future__ import annotations
from typing import Dict, List, Tuple, Optional
from pprint import pprint
from math import inf
from functools import partial, cache


def get_valves_neighbors_rates(
    file: str,
) -> Tuple[Dict[str, List[str], Dict[str, int]]]:
    valves_neighbors = dict()
    valves_rates = dict()
    with open("./puzzles/day_16/" + file, mode="r") as input_file:
        for line in input_file.readlines():
            stripped_line = line.strip()
            name = stripped_line[6:8]
            rate = int(stripped_line.split("=")[1].split(";")[0])
            neighbors = (
                stripped_line.replace("valves", "valve").split("valve ")[1].split(", ")
            )
            valves_neighbors[name] = neighbors
            valves_rates[name] = rate
    return valves_neighbors, valves_rates


def calc_valves_dists(
    initial_valve: str,
    valves_neighbors: Dict[str, List[str]],
    relevant_valves=None,
) -> Dict[str, float]:

    unvisited_valves = list(valves_neighbors.keys())
    distances = {valve: inf for valve in unvisited_valves}
    visited_valves = []

    current_valve = initial_valve
    distances[current_valve] = 0

    while unvisited_valves:

        neighbors = valves_neighbors[current_valve]
        unvisited_neighbors = [
            neighbor for neighbor in neighbors if neighbor not in visited_valves
        ]

        for unvisited_neighbor in unvisited_neighbors:
            if distances[current_valve] + 1 < distances[unvisited_neighbor]:
                distances[unvisited_neighbor] = distances[current_valve] + 1

        visited_valves.append(current_valve)
        unvisited_valves.remove(current_valve)

        next_possible_valves = [
            valve for valve in unvisited_valves if distances[valve] < inf
        ]

        if next_possible_valves != []:
            current_valve = next_possible_valves[0]

    del distances[initial_valve]

    if relevant_valves:
        distances = {
            key: value for key, value in distances.items() if key in relevant_valves
        }

    return distances


def get_valves_dists_rates(
    file, only_relevant=None
) -> Tuple[Dict[Dict[str, int]], Dict[str, int]]:
    valves_neighbors, valves_rates = get_valves_neighbors_rates(file)
    valves_dists = {
        valve: calc_valves_dists(valve, valves_neighbors)
        for valve, neighbors in valves_neighbors.items()
    }

    if only_relevant is not None:
        if isinstance(only_relevant, str):
            valves_dists = {
                valve: {
                    other_valve: distance
                    for other_valve, distance in distances.items()
                    if (valves_rates[other_valve] != 0) | (other_valve == only_relevant)
                }
                for valve, distances in valves_dists.items()
                if (valves_rates[valve] != 0) | (valve == only_relevant)
            }
            valves_rates = {
                valve: rate
                for valve, rate in valves_rates.items()
                if (rate != 0) | (valve == only_relevant)
            }
        elif isinstance(only_relevant, bool):
            if only_relevant == True:
                valves_dists = {
                    valve: {
                        other_valve: distance
                        for other_valve, distance in distances.items()
                        if (valves_rates[other_valve] != 0)
                    }
                    for valve, distances in valves_dists.items()
                    if (valves_rates[valve] != 0)
                }
                valves_rates = {
                    valve: rate for valve, rate in valves_rates.items() if (rate != 0)
                }

    return valves_dists, valves_rates


def get_dists_here_next_dists(
    valve: str, dists: Dict[str, Dict[str, int]]
) -> Tuple[int, Dict[str, Dict[str, int]]]:

    dists_here = dists[valve]
    next_dists = {
        valve_: {
            valve__: distance
            for valve__, distance in distances.items()
            if valve__ != valve
        }
        for valve_, distances in dists.items()
        if valve_ != valve
    }

    return dists_here, next_dists


def get_rate_here_next_rates(
    valve: str, rates: Dict[str, int]
) -> Tuple[int, Dict[str, int]]:

    rate_here = rates[valve]
    next_rates = {valve_: rate for valve_, rate in rates.items() if valve_ != valve}

    return rate_here, next_rates


def release_max_pressure(
    valve: str,
    dists: Dict[str, Dict[str, int]],
    rates: Dict[str, int],
    time_left,
    total_time: Optional[int] = None,
) -> Tuple[str, int]:

    # if time_left < 2:
    #     return "", 0

    if total_time is None:
        total_time = time_left

    dists_here, next_dists = get_dists_here_next_dists(valve, dists)
    rate_here, next_rates = get_rate_here_next_rates(valve, rates)

    time_here = 0

    if rate_here > 0:
        time_here = 1

    pressure_here = (time_left - time_here) * rate_here
    str_here = (
        " "
        + valve
        + "@t="
        + str(total_time - (time_left - time_here))
        + "/p="
        + str(pressure_here)
    )

    next_pressure = 0
    next_str = ""

    for next_valve, dist_to_next_valve in dists_here.items():

        next_time_left = time_left - time_here - dist_to_next_valve

        if next_time_left < 2:
            continue

        next_valve_str, next_valve_pressure = release_max_pressure(
            valve=next_valve,
            dists=next_dists,
            rates=next_rates,
            time_left=next_time_left,
            total_time=total_time,
        )

        if next_valve_pressure >= next_pressure:
            next_str = next_valve_str
            next_pressure = next_valve_pressure

    return str_here + next_str, pressure_here + next_pressure


def part1(file: str) -> None:

    current_valve = "AA"
    dists, rates = get_valves_dists_rates(file, only_relevant=current_valve)

    pprint(dists)

    print(release_max_pressure(current_valve, dists, rates, 30))

    # 1434 is wrong
    # AA@t=0/p=0 UM@t=3/p=135 VO@t=7/p=138 JF@t=10/p=200
    # AH@t=14/p=368 HZ@t=17/p=260 VR@t=20/p=240 GL@t=24/p=66 XN@t=27/p=27'
    # 1434)


def part2(file: str) -> None:
    ...


def main(file: str) -> None:
    part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
