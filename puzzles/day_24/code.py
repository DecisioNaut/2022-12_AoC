from __future__ import annotations
from collections import defaultdict
from functools import cache
from math import inf, lcm
from pprint import pprint


def get_data(file: str):
    with open("./puzzles/day_24/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def get_valley_data(file):

    rows = 0
    cols = 0
    row_blizzes = defaultdict(list)
    col_blizzes = defaultdict(list)

    for row, data in enumerate(get_data(file)):
        rows = max(row, rows)
        for col, sign in enumerate(data):
            cols = max(col, cols)
            if sign == ">":
                row_blizzes[row].append((col, False))
            elif sign == "<":
                row_blizzes[row].append((col, True))
            elif sign == "v":
                col_blizzes[col].append((row, False))
            elif sign == "^":
                col_blizzes[col].append((row, True))
            else:
                row_blizzes[row] += []
                col_blizzes[col] += []

    rows = rows + 1
    cols = cols + 1

    return rows, cols, row_blizzes, col_blizzes


rows, cols, row_blizzes, col_blizzes = get_valley_data("data.txt")


times = lcm(
    rows - 2, cols - 2
)  # as blizzes can only incrementally move from 1..(rows-1) or 1...(cols-1) after this everything repeats


def is_start(row, col, time: int | None = None) -> bool:
    return (row == 0) & (col == 1)


def is_target(row, col, time: int | None = None) -> bool:
    return (row == rows - 1) & (col == cols - 2)


def dist_to_target(row, col, time) -> int:
    return abs(row - (rows - 1)) + abs(col - (cols - 2)) + abs(time)


def dist_to_start(row, col, time) -> int:
    return abs(row) + abs(col - 1) + abs(time)


@cache
def hits_wall(row, col) -> bool:
    # start or target hole are not walls
    if is_start(row, col) | is_target(row, col):
        return False
    # all other positions at the edge of the valley
    else:
        return not (0 < row < (rows - 1)) & (0 < col < (cols - 1))


@cache
def move_blizz(
    time: int, pos: int, direction_row: bool = True, reverse: bool = False
) -> int:
    blizz_pos_minus_1 = pos - 1  # to let blizzes start from 0
    blizz_pos_modulo: int = (
        cols - 2 if direction_row else rows - 2
    )  # as blizzes can be at 1..(rows-1) or 1..(cols-1)
    direction: int = 1 - 2 * reverse  # -1 if reversed else 1
    return (
        blizz_pos_minus_1 + direction * time
    ) % blizz_pos_modulo + 1  # adding back the 1


def hits_blizz(row, col, time) -> bool:

    modulated_time = time % times

    relevant_row_blizzes = [
        (
            row,
            move_blizz(
                time=modulated_time,
                pos=pos,
                direction_row=True,
                reverse=reverse,
            ),
        )
        for (pos, reverse) in row_blizzes[row]
    ]

    relevant_col_blizzes = [
        (
            move_blizz(
                time=modulated_time,
                pos=pos_reverse_tuple[0],
                direction_row=False,
                reverse=pos_reverse_tuple[1],
            ),
            col,
        )
        for pos_reverse_tuple in col_blizzes[col]
    ]

    blizzes = relevant_row_blizzes + relevant_col_blizzes

    return (row, col) in blizzes


@cache
def is_open(row, col, time) -> bool:
    if hits_wall(row, col):
        return False
    else:
        return not hits_blizz(row, col, time)


def print_status(time):
    array = [["." for col in range(cols)] for row in range(rows)]
    for row, col_data in enumerate(array):
        for col, sign in enumerate(col_data):
            if hits_wall(row, col):
                array[row][col] = "#"
            if hits_blizz(row, col, time):
                array[row][col] = "+"
    print("\n".join(["".join(row) for row in array]) + "\n")


def get_neighbors(row, col, time):
    return [
        pos
        for pos in [
            (row, col, time + 1),
            (row + 1, col, time + 1),
            (row - 1, col, time + 1),
            (row, col + 1, time + 1),
            (row, col - 1, time + 1),
        ]
        if is_open(*pos)
    ]


unvisited_positions = []
distances = defaultdict()
visited_positions = []

current_position = (0, 1, 0)
unvisited_positions.append(current_position)
distances[current_position] = 0


while not is_target(*current_position):

    unvisited_positions = sorted(
        unvisited_positions, key=lambda position: dist_to_target(*position)
    )

    current_position = unvisited_positions.pop(0)
    current_distance = distances[current_position]

    neighbors = get_neighbors(*current_position)
    #  print(neighbors)

    for neighbor in neighbors:
        if neighbor not in unvisited_positions:
            unvisited_positions.append(neighbor)
            distances[neighbor] = current_distance + 1
        else:
            distances[neighbor] = min(distances[neighbor], current_distance + 1)

    visited_positions.append(current_position)


first_trip_time = distances[current_position]

print("From Start to End", first_trip_time)
print("An Elve forgot his snack!?!")

unvisited_positions = []
distances = defaultdict()
visited_positions = []

current_position = (rows - 1, cols - 2, first_trip_time)
assert is_target(*current_position)
unvisited_positions.append(current_position)
distances[current_position] = 0

while not is_start(*current_position):

    unvisited_positions = sorted(
        unvisited_positions,
        key=lambda position: dist_to_start(*position),
    )

    current_position = unvisited_positions.pop(0)
    current_distance = distances[current_position]

    neighbors = get_neighbors(*current_position)

    for neighbor in neighbors:
        if neighbor not in unvisited_positions:
            unvisited_positions.append(neighbor)
            distances[neighbor] = current_distance + 1
        else:
            distances[neighbor] = min(distances[neighbor], current_distance + 1)

    visited_positions.append(current_position)

second_trip_time = distances[current_position]

print("Back to the Start", second_trip_time)
print("Collecting Snack...")

unvisited_positions = []
distances = defaultdict()
visited_positions = []

current_position = (0, 1, first_trip_time + second_trip_time)
unvisited_positions.append(current_position)
distances[current_position] = 0


while not is_target(*current_position):

    unvisited_positions = sorted(
        unvisited_positions, key=lambda position: dist_to_target(*position)
    )

    current_position = unvisited_positions.pop(0)
    current_distance = distances[current_position]

    neighbors = get_neighbors(*current_position)
    #  print(neighbors)

    for neighbor in neighbors:
        if neighbor not in unvisited_positions:
            unvisited_positions.append(neighbor)
            distances[neighbor] = current_distance + 1
        else:
            distances[neighbor] = min(distances[neighbor], current_distance + 1)

    visited_positions.append(current_position)


third_trip_time = distances[current_position]

print("From Start to End ... again!!", third_trip_time)
print(
    "This now took",
    first_trip_time + second_trip_time + third_trip_time,
    "you Elve, you!!",
)
