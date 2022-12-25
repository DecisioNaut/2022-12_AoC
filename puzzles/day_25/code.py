from __future__ import annotations

from typing import List


def get_data(file: str):
    with open("./puzzles/day_25/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


DECODE = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
ENCODE = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}


def decode(encoded_num: str) -> int:

    num = 0
    for i, elm in enumerate(list(reversed(list(encoded_num)))):
        num += int(5**i) * DECODE[elm]

    return num


def encode(num: int):
    base5_array = []
    while num:
        base5_array.append(num % 5)
        num = num // 5

    mod_base5_array = base5_array.copy()

    for i in range(len(mod_base5_array) - 1):
        if mod_base5_array[i] > 2:
            mod_base5_array[i] -= 5
            mod_base5_array[i + 1] += 1

    if mod_base5_array[-1] > 2:
        mod_base5_array[-1] -= 5
        mod_base5_array.append(1)

    encoded = ""
    for elm in reversed(mod_base5_array):
        encoded += ENCODE[elm]

    return encoded


def part1(file: str) -> None:

    total_decoded = 0

    for data in get_data(file):
        total_decoded += decode(data)

    encoded = encode(total_decoded)

    print("Part 1:", encoded)


def part2(file: str) -> None:

    print(
        "Part 2:",
    )


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
