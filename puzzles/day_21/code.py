from __future__ import annotations

from typing import List, Optional, Callable, Union, Dict
from operator import add, sub, mul, truediv
from pprint import pprint


def get_data(file: str):
    with open("./puzzles/day_21/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def monkey_vals(
    raw_value: str,
) -> Union[Dict[str, int], Dict[str, Union[str, Callable]]]:

    operation_dict = {"+": add, "-": sub, "*": mul, "/": truediv}

    comps = raw_value.split(" ")

    if len(comps) == 1:
        return {"number": int(comps[0])}

    else:
        return {
            "operation": operation_dict[comps[1]],
            "left": comps[0],
            "right": comps[2],
        }


def make_monkey_dict(file: str):
    monkey_dict = dict()
    for data in get_data(file):
        key, raw_value = data.split(": ")
        monkey_dict[key] = monkey_vals(raw_value)
    return monkey_dict


class Monkey:
    def __init__(
        self,
        name: str,
        number: Optional[int] = None,
        left: Optional[Monkey] = None,
        operation: Optional[
            Callable[[Union[Monkey, int], Union[Monkey, int]], int]
        ] = None,
        right: Optional[Monkey] = None,
    ) -> None:
        self.name = name
        self.number = number
        self.left = left
        self.operation = operation
        self.right = right

    def __call__(self):
        if self.number:
            return self.number
        else:
            return int(self.operation(self.left(), self.right()))

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class MonkeyGroup:
    def __init__(self, monkey_dict) -> None:
        self.monkeys: List[Monkey] = [Monkey(name) for name in monkey_dict.keys()]

        for name, properties in monkey_dict.items():
            for property, value in properties.items():
                if property == "number":
                    self[name].number = value
                elif property == "left":
                    self[name].left = self[value]
                elif property == "operation":
                    self[name].operation = value
                elif property == "right":
                    self[name].right = self[value]
                else:
                    raise KeyError

    def __getitem__(self, name):
        for monkey in self.monkeys:
            if monkey.name == name:
                return monkey
        raise KeyError


def part1(file: str) -> None:
    monkey_dict = make_monkey_dict(file)
    monkey_group = MonkeyGroup(monkey_dict)

    print("Part 1:", monkey_group["root"]())


def part2(file: str) -> None:
    data = get_data(file)
    print(
        "Part 2:",
    )


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
