from __future__ import annotations

from typing import List, Optional
from graphlib import TopologicalSorter, CycleError
from functools import total_ordering
from pprint import pprint
from collections import OrderedDict


def get_data(file: str):
    with open("./puzzles/day_16/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


@total_ordering
class Valve:
    def __init__(
        self,
        name: str,
        ppm: int,
        open: bool = False,
        tunnels: Optional[List[Valve]] = None,
    ) -> None:
        self._name = name
        self._ppm = ppm
        self._open = open
        self._tunnels = tunnels

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
        # if not (self._tunnels is None):
        #    raise ValueError(f"Valve {self._name} already has tunnels!")
        self._tunnels = tunnels

    def __eq__(self, other):
        return self._name == other._name

    def __lt__(self, other):
        if self._ppm == other._ppm:
            return self._name < other._name
        else:
            return self._ppm < other._ppm

    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        return self._name

    __repr__ = __str__


def part1(file: str) -> None:

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

    valves_graph_dict = OrderedDict()
    for valve in valves:
        valves_graph_dict[valve] = valve.tunnels

    pprint(valves_graph_dict)


def part2(file: str) -> None:
    data = get_data(file)
    ...


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
