from __future__ import annotations

from typing import List, Optional
from functools import total_ordering
from pprint import pprint
from collections import OrderedDict
from math import inf
from itertools import permutations


def get_data(file: str):
    with open("./puzzles/day_16/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def get_valves(file: str) -> List[Valve]:

    valves_graph_dict = dict()

    for data in get_data(file):
        valve_name_ppm_str, tunnel_str_list_str = (
            data.replace("Valve ", "")
            .replace(" has flow rate", "")
            .replace(" tunnels lead to valves ", "")
            .replace(" tunnel leads to valve ", "")
        ).split(";")
        valve_name, ppm_str = valve_name_ppm_str.split("=")
        valve = Valve(valve_name, int(ppm_str))
        tunnel_str_list = tunnel_str_list_str.split(", ")
        valves_graph_dict[valve] = tunnel_str_list

    valves = []

    for valve, tunnels_str_list in valves_graph_dict.items():
        tunnels = []
        for tunnels_str in tunnels_str_list:
            for test_valve in valves_graph_dict.keys():
                if test_valve.name == tunnels_str:
                    tunnels.append(test_valve)
        tunnels = list(reversed(sorted(tunnels)))
        valve.tunnels = tunnels
        valves.append(valve)
        valves_graph_dict[valve] = tunnels

    valves = list(reversed(sorted(valves)))

    return valves


@total_ordering
class Valve:
    def __init__(
        self,
        name: str,
        ppm: int,
    ) -> None:
        self._name = name
        self._ppm = ppm
        self._open: bool = False
        self._tunnels: Optional[List[Valve]] = None

    @property
    def name(self):
        return self._name

    @property
    def ppm(self):
        return self._ppm

    @property
    def open(self):
        return self._open

    @open.setter
    def open(self, true):
        if self._open:
            raise ValueError(f"Valve {self._name} is already open!")
        self._open = True

    @property
    def is_closed(self):
        return not (self._open)

    @property
    def tunnels(self):
        return self._tunnels

    @tunnels.setter
    def tunnels(self, tunnels: List[Valve]):
        self._tunnels = tunnels

    def __eq__(self, other):
        return self._name == other._name

    def __lt__(self, other):
        if self._ppm == other._ppm:
            return self._name < other._name
        else:
            return self._ppm < other._ppm

    def __contains__(self, others: List[Valve]):
        for other in others:
            if other == self:
                return True
        return False

    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        return f"{self._name}{' ' if self._open else '['}{str(self._ppm).zfill(2).replace('00','__')}{' ' if self._open else ']'}"

    __repr__ = __str__


def get_distances(valve: Valve) -> OrderedDict[Valve]:

    visited_valves: List[Valve] = []
    unvisited_valves: List[Valve] = []
    distances = OrderedDict()

    def add_to_visited_valves(valve: Valve) -> None:
        visited_valves.append(valve)

    def add_to_unvisited_valves_if_not_visited(tunnels: List[Valve]) -> None:
        for tunnel in tunnels:
            if not (tunnel in visited_valves):
                unvisited_valves.append(tunnel)
                distances[tunnel] = inf

    def update_distance_if_not_visited(valve: Valve, new_distance: int) -> None:
        if valve in unvisited_valves:
            current_distance = distances[valve]
            if new_distance < current_distance:
                distances[valve] = new_distance

    add_to_unvisited_valves_if_not_visited([valve] + valve.tunnels)
    update_distance_if_not_visited(valve, 0)

    while unvisited_valves != []:
        current_valve = unvisited_valves.pop(0)
        current_distance = distances[current_valve]
        current_tunnels = current_valve.tunnels
        add_to_unvisited_valves_if_not_visited(current_tunnels)
        for tunnel in current_tunnels:
            update_distance_if_not_visited(tunnel, current_distance + 1)
        add_to_visited_valves(current_valve)

    return distances


def get_relevant_distances(valve: Valve) -> OrderedDict[Valve]:

    relevant_distances = OrderedDict()
    distances = get_distances(valve)

    for valve, distance in distances.items():
        if valve.ppm > 0:
            relevant_distances[valve] = distance

    return relevant_distances


def maximise_pressure_released(
    valve: Valve,
    valves_visited: Optional[List[Valve]] = None,
    initial_pressure_released: int = 0,
    time_left: int = 30,
) -> int:

    valve.relevant_distances = get_relevant_distances(valve)

    if valves_visited is None:
        valves_visited = []

    max_pressure_released = initial_pressure_released

    unvisited_valves = [
        valve_
        for valve_ in valve.relevant_distances.keys()
        if not (valve in valves_visited)
    ]

    relevant_valves = [
        valve_
        for valve_ in unvisited_valves
        if valve.relevant_distances[valve_]
        < time_left - 2  # 1 to move there + 1 to have an effect from opening
    ]

    if relevant_valves == []:

        return max_pressure_released

    else:

        for relevant_valve in relevant_valves:

            time_for_travel = valve.relevant_distances[relevant_valve]
            time_for_opening = 1
            new_time_left = time_left - time_for_travel - time_for_opening

            new_pressure_released = (
                initial_pressure_released + relevant_valve.ppm * new_time_left
            )

            new_valves_visited = [relevant_valve] + valves_visited

            next_new_pressure_released = new_pressure_released

            for new_valve in relevant_valve.tunnels:

                test_new_pressure_released = maximise_pressure_released(
                    new_valve, new_valves_visited, new_pressure_released, new_time_left
                )

                if test_new_pressure_released > next_new_pressure_released:

                    next_new_pressure_released = test_new_pressure_released

            if new_pressure_released > max_pressure_released:

                max_pressure_released = new_pressure_released

        return max_pressure_released


def part1(file: str) -> None:

    valves = get_valves(file)

    aa = valves[-1]
    assert aa.name == "AA"
    assert aa.ppm == 0
    # Monkey patch distances
    aa.relevant_distances = get_relevant_distances(aa)

    relevant_valves = [aa]

    for relevant_valve in aa.relevant_distances:
        # Monkey patch distances
        relevant_valve.distances = get_relevant_distances(relevant_valve)
        relevant_valves.append(relevant_valve)

    max_pressure_released = maximise_pressure_released(relevant_valves[0])

    print("Part 1", max_pressure_released)


""" 
    permutations_count = 0
    for permutation in permutations(relevant_valves):
        permutations_count += 1
        if permutations_count % 1_000_000 == 0:
            print(int(permutations_count / 1_000_000))
    print(permutations_count)
 """


def part2(file: str) -> None:
    data = get_data(file)
    ...


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("example.txt")
