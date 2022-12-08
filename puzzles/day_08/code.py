from __future__ import annotations

from typing import List
from itertools import takewhile
from pprint import pprint


def get_data(file: str) -> List[List[int]]:
    data = []
    with open("./puzzles/day_08/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            data.append([int(item) for item in line.strip()])
    return data


def is_visible(data: List[List[int]], i: int, j: int) -> bool:

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


def scenic_score(data, i, j):

    compare_val = data[i][j]

    height = len(data)
    width = len(data[0])

    def evaluate_view(potential_view: List[int]) -> int:
        def lt_compare_val(x):
            return x < compare_val

        restricted_view = list(takewhile(lt_compare_val, potential_view))
        effective_reach_of_view = len(restricted_view) + (
            1 if len(potential_view) != len(restricted_view) else 0
        )

        return effective_reach_of_view

    # to top
    potential_view_to_top = [data[k][j] for k in reversed(range(i))]
    to_top = evaluate_view(potential_view_to_top)

    # to left
    potential_view_to_left = [data[i][k] for k in reversed(range(j))]
    to_left = evaluate_view(potential_view_to_left)

    # to right
    potential_view_to_right = [data[i][k] for k in range(j + 1, width)]
    to_right = evaluate_view(potential_view_to_right)

    # to bottom
    potential_view_to_bottom = [data[k][j] for k in range(i + 1, height)]
    to_bottom = evaluate_view(potential_view_to_bottom)

    return to_left * to_right * to_top * to_bottom


def main():

    data = get_data("part_1_data.txt")

    visibles = 0
    max_scenic_score = 0

    for i in range(len(data)):
        for j in range(len(data[0])):
            if is_visible(data, i, j):
                visibles += 1
                max_scenic_score = max([max_scenic_score, scenic_score(data, i, j)])

    print("Part 1:", visibles)
    print("Part 2:", max_scenic_score)

    scenic_score(data, 3, 2)


if __name__ == "__main__":

    main()
