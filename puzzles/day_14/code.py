from enum import Enum


def get_data(file: str) -> str:
    with open("./puzzles/day_14/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def get_rock_line_edges_list(file: str):

    rock_line_edges_list = []
    for data in get_data(file):
        rock_line_edges_strings = data.split(" -> ")
        rock_line_edges_string_pairs = [
            rock_line_edges_string.split(",")
            for rock_line_edges_string in rock_line_edges_strings
        ]
        rock_line_edges = [
            [int(rock_line_edges[0]), int(rock_line_edges[1])]
            for rock_line_edges in rock_line_edges_string_pairs
        ]
        rock_line_edges_list.append(rock_line_edges)

    return rock_line_edges_list


def get_rock_lines(rock_line_edges_list):

    for rock_line_edges in rock_line_edges_list:
        for index in range(len(rock_line_edges) - 1):
            ...


class Place(Enum):
    air = 0
    sand = 1
    rock = 2


def part_1(file: str):

    coords = get_rock_line_edges_list(file)

    print("Part 1:", coords)


def part_2(file: str):
    print(
        "Part 2:",
    )


def main(file: str):
    part_1(file)
    part_2(file)


if __name__ == "__main__":
    main("example.txt")
