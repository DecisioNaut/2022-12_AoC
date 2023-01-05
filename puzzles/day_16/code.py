from __future__ import annotations

from functools import cache
from itertools import combinations
from math import inf

# from datetime import datetime
from typing import Optional, NamedTuple, Type, Generator, Callable


Times = Type


def get_valves_neighbors_rates(
    file: str,
) -> tuple[dict[str, list[str]], dict[str, int]]:
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


def calc_distances(file: str) -> dict[str, dict[str, int]]:

    neighbors, _ = get_valves_neighbors_rates(file)
    valves = list(neighbors.keys())
    distances: dict[str, dict[str, int]] = {}

    for valve in valves:

        visited_valves = []
        unvisited_valves = [valve_ for valve_ in valves]
        current_distances = {valve_: inf for valve_ in unvisited_valves}

        current_valve = valve
        current_distances[current_valve] = 0

        while unvisited_valves:

            available_neigbors = [
                valve
                for valve in neighbors[current_valve]
                if valve not in visited_valves
            ]

            for valve_ in available_neigbors:
                if current_distances.get(valve_) is None:
                    current_distances[valve_] = current_distances[current_valve] + 1
                else:
                    current_distances[valve_] = min(
                        current_distances[valve_],
                        current_distances[current_valve] + 1,
                    )

            visited_valves.append(current_valve)
            unvisited_valves.remove(current_valve)

            distances_of_valves_not_visited = {
                valve_: dist
                for valve_, dist in current_distances.items()
                if valve_ not in visited_valves
            }

            if distances_of_valves_not_visited:

                current_valve = sorted(
                    distances_of_valves_not_visited.keys(),
                    key=lambda valve: distances_of_valves_not_visited[valve],
                )[0]

        current_distances_int: dict[str, int] = {
            valve_: int(dist) for valve_, dist in current_distances.items()
        }
        distances[valve] = current_distances_int

    return distances


def clean_valves_rates_distances(
    file,
) -> tuple[list[str], dict[str, int], dict[str, dict[str, int]]]:

    neighbors, rates = get_valves_neighbors_rates(file)
    valves = list(neighbors.keys())
    distances = calc_distances(file)

    clean_valves = sorted(
        [valve_ for valve_ in valves if (rates[valve_] != 0) | (valve_ == "AA")]
    )

    clean_rates = {
        valve_: rate for valve_, rate in rates.items() if (valve_ == "AA") | (rate != 0)
    }

    clean_distances = {
        current_valve: {
            other_valve: distance
            for other_valve, distance in current_distances.items()
            if (other_valve == "AA") | (rates[other_valve] != 0)
        }
        for current_valve, current_distances in distances.items()
        if (current_valve == "AA") | (rates[current_valve] != 0)
    }
    return clean_valves, clean_rates, clean_distances


def make_TimesClass_and_optimizer(
    valves: list[str],
    rates: dict[str, int],
    distances: dict[str, dict[str, int]],
    time_available: int = 30,
) -> tuple[Times, Callable]:

    valve_times_types = [(valve, Optional[int]) for valve in valves]

    class Times(NamedTuple("Times", valve_times_types)):
        """Somewhat hacky kind of class to define the state of the voyage through the maze"""

        __slots__ = ()

        def __new__(cls, **kwargs):
            """Set non given times at valves to None"""
            for key in kwargs:
                if key not in valves:
                    raise KeyError("Keys must be in valves")
            if len(kwargs.values()) != len(set(kwargs.values())):
                raise ValueError("Times provided must be unique")
            if min(kwargs.values()) < 1:
                raise ValueError("Lowest time must be 1")
            if max(kwargs.values()) >= time_available:
                raise ValueError(
                    "Highest time must be one below time_available to have an effect on pressure release"
                )
            values = {
                valve: None if valve not in kwargs.keys() else kwargs[valve]
                for valve in valves
            }
            return super().__new__(cls, **values)

        def __init__(self, **kwargs):
            return super().__init__()

        @property
        def visited_valves(self) -> list[str]:
            """visited valves sorted in increasing order of time of visit"""
            times: dict[str, int] = {
                valve: time
                for valve, time in self._asdict().items()
                if time is not None
            }
            return sorted(times.keys(), key=lambda valve: times[valve])

        @property
        def unvisited_valves(self) -> list[str]:
            """all valves with time set to None"""
            times: dict[str, int] = {
                valve: time for valve, time in self._asdict().items() if time is None
            }
            return sorted(times.keys())

        @property
        def available_valves(self) -> list[str]:
            return [
                valve
                for valve in self.unvisited_valves
                if distances[self.current_valve][valve]
                < time_available - self.current_time - 1
            ]

        @property
        def current_valve(self) -> str:
            """valve with the highest time of visit"""
            return self.visited_valves[-1]

        @property
        def current_time(self) -> int:
            """highest time of visit"""
            return self._asdict()[self.current_valve]

        @property
        def current_times_dict(self) -> dict[str, int]:
            return {
                valve: time
                for valve, time in self._asdict().items()
                if time is not None
            }

        @property
        def next_times_dicts(self) -> list[dict[str, int]]:
            current_valve = self.current_valve
            current_valve_openable = rates[current_valve] != 0
            current_time = self.current_time
            available_valves = self.available_valves
            next_times = [
                {
                    valve: (
                        current_time
                        + current_valve_openable
                        + distances[current_valve][valve]
                    )
                }
                for valve in available_valves
            ]
            return next_times

        @property
        def next_times(self) -> list[Times]:
            current_times_dict = self.current_times_dict
            next_times_dicts = self.next_times_dicts
            return [
                Times(**(current_times_dict | next_time_dict))
                for next_time_dict in next_times_dicts
            ]

        @property
        def flows(self) -> dict[str, int]:
            valves = self.visited_valves
            return {
                valve: (time_available - self._asdict()[valve]) * rates[valve]
                for valve in valves
            }

        @property
        def total_flow(self) -> int:
            return sum(list(self.flows.values()))

        def __repr__(self) -> str:
            return ", ".join(
                [
                    f"t={self.current_times_dict[valve]}:{valve}"
                    for valve in self.visited_valves
                ]
            )

    @cache
    def optimizer(times: Times) -> int:
        best_total_flow = times.total_flow
        if times.next_times != []:
            for next_times in times.next_times:
                next_total_flow = optimizer(next_times)
                best_total_flow = max(best_total_flow, next_total_flow)
        return best_total_flow

    return Times, optimizer


def select_from_valves(valves: list[str]) -> Generator:
    tuple[int]
    for i in range(0, (len(valves) - 1) // 2 + 1):
        for combination in combinations(valves[1:], i):
            left = [valves[0]] + [valve for valve in combination]
            right = [valves[0]] + [
                valve for valve in valves[1:] if valve not in combination
            ]
            yield left, right


def select_rates(selected_valves: list[str], rates: dict[str, int]) -> dict[str, int]:
    return {valve: rate for valve, rate in rates.items() if valve in selected_valves}


def select_distances(
    selected_valves: list[str], distances: dict[str, dict[str, int]]
) -> dict[str, dict[str, int]]:
    return {
        valve: {
            valve_: dist for valve_, dist in dists.items() if valve_ in selected_valves
        }
        for valve, dists in distances.items()
        if valve in selected_valves
    }


def part1(file) -> None:

    valves, rates, distances = clean_valves_rates_distances(file)
    Times, optimizer = make_TimesClass_and_optimizer(
        valves, rates, distances, time_available=30
    )

    times = Times(AA=1)
    print("Part 1:", optimizer(times))


def part2(file) -> None:

    valves, rates, distances = clean_valves_rates_distances(file)
    time_available = 26

    max_flow = 0

    for my_valves, elephant_valves in select_from_valves(valves):

        my_rates = select_rates(my_valves, rates)
        my_distances = select_distances(my_valves, distances)
        myTimes, my_optimizer = make_TimesClass_and_optimizer(
            my_valves, my_rates, my_distances, time_available
        )

        my_times = myTimes(AA=1)
        my_flow = my_optimizer(my_times)

        elephant_rates = select_rates(elephant_valves, rates)
        elephant_distances = select_distances(elephant_valves, distances)
        elephantTimes, elephant_optimizer = make_TimesClass_and_optimizer(
            elephant_valves, elephant_rates, elephant_distances, time_available
        )

        elephant_times = elephantTimes(AA=1)
        elephant_flow = elephant_optimizer(elephant_times)

        max_flow = max(max_flow, my_flow + elephant_flow)

    print("Part 2:", max_flow)


def main() -> None:
    file = "data.txt"
    part1(file)
    part2(file)


if __name__ == "__main__":
    main()
