from __future__ import annotations

from typing import List, Union, Tuple, Literal, Optional
from pprint import pprint


def get_data(file: str) -> str:
    with open("./puzzles/day_22/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.replace(f"\n", "")


def get_commands_data(line: str) -> List[Union[int, str]]:

    intermediate_list = line.replace("R", ",R,").replace("L", ",L,").split(",")

    resulting_list = []

    for element in intermediate_list:
        try:
            resulting_list.append(("move", int(element)))
        except ValueError:
            resulting_list.append(("turn", element))

    return resulting_list


def get_lists_for_further_processing(file: str):

    for data in get_data(file):
        if data == "":
            pass
        elif data.startswith(" ") | data.startswith(".") | data.startswith("#"):
            yield list(data)
        else:
            yield get_commands_data(data)


def get_grove_command_data(file: str):

    uncleaned_data = []

    for element in get_lists_for_further_processing(file):
        uncleaned_data.append(element)

    commands_data = uncleaned_data.pop(-1)

    width_grove = 0

    for element in uncleaned_data:
        width_grove = max(width_grove, len(element))

    for element in uncleaned_data:
        if len(element) < width_grove:
            element += [
                " " for further_elements in range(0, width_grove - len(element))
            ]

    grove_data = uncleaned_data

    return grove_data, commands_data


class Map:
    # Set of Location
    # List of Objects
    ...


def part1(file: str) -> None:

    grove_data, commands_data = get_grove_command_data(file)

    pprint(grove_data, compact=False, width=100)

    print(
        "Part 1:",
    )


def part2(file: str) -> None:
    print(
        "Part 2:",
    )


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("example.txt")
