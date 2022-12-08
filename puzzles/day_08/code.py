from __future__ import annotations

from typing import List, Tuple
from itertools import accumulate
from copy import deepcopy
from pprint import pprint


def get_data(file: str) -> List[List[int]]:
    data = []
    with open("./puzzles/day_08/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            data.append([int(item) for item in line.strip()])
    return data


def is_visible(data, i, j):

    target_val = data[i][j]

    height = len(data)
    width = len(data[0])

    if (i == 0) | (i == height - 1) | (j == 0) | (j == width - 1):
        return True
    else:
        from_left = target_val > max([data[i][k] for k in range(j)])
        from_right = target_val > max([data[i][k] for k in range(j + 1, width)])
        from_top = target_val > max([data[k][j] for k in range(i)])
        from_bottom = target_val > max([data[k][j] for k in range(i + 1, height)])
        return from_left | from_right | from_top | from_bottom


def main():

    data = get_data("part_1_data.txt")

    visibles = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            visibles += is_visible(data, i, j)

    print("Part 1:", visibles)


if __name__ == "__main__":
    main()
