from collections import namedtuple
from pprint import pprint
from typing import Tuple, NamedTuple


class Valve(NamedTuple):
    name: str
    rate: int
    tunnels: Tuple[str, ...]


valve = Valve(name="AA", rate=0, tunnels=("DD", "II", "BB"))


def get_valves(file: str):
    valves: Tuple[Valve, ...] = tuple()
    with open("./puzzles/day_16/" + file, mode="r") as f:
        for line in f.readlines():
            name: str = line[6:8]
            rate: int = int(line.split(";")[0].split("=")[1])
            tunnels: Tuple[str, ...] = tuple(
                line.replace("valves ", "valve ").split("valve ")[1].strip().split(", ")
            )
            valves = valves + (Valve(name=name, rate=rate, tunnels=tunnels),)
    return valves


valves = get_valves("example.txt")

pprint(valves)
