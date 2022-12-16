from __future__ import annotations
from typing import List, Tuple
from math import inf


def get_data(file: str) -> str:
    with open("./puzzles/day_12/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


class Position:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

    def __repr__(self) -> str:
        return f"Position(row={self.row}, col={self.col})"

    def __str__(self) -> str:
        return f"[{self.row}, {self.col}]"

    def __add__(self, other: Position) -> Position:
        row = self.row + other.row
        col = self.col + other.col
        return Position(row, col)

    def __iadd__(self, other: Position) -> None:
        self.row = self.row + other.row
        self.col = self.col + other.col

    @property
    def as_tuple(self):
        return self.row, self.col


class DijkstraMap:
    def __init__(
        self, heightmap: List[List[int]], startpos: Position, downhill: bool = False
    ) -> None:

        # Setting up basic data
        self.heightmap: List[List[bool]] = heightmap

        # 1. Mark all nodes as unvisited
        self.visitedmap: List[List[bool]] = [
            [False for col in row] for row in heightmap
        ]

        # 2. Assign every node a tentative distance inf, except startpos where it's 0
        self.distancemap: List[List[float]] = [
            [inf for col in row] for row in heightmap
        ]
        self.set_distance(startpos, 0.0)

        # Setting up a deque for positions to be evaluated
        self.to_be_evaluated: List[Position] = [startpos]

        self.downhill = downhill

    def get_height(self, pos: Position) -> int:
        row, col = pos.as_tuple
        return self.heightmap[row][col]

    def is_accessible(self, from_pos: Position, to_pos: Position) -> bool:
        if not (self.downhill):
            return self.get_height(to_pos) - 1 <= self.get_height(from_pos)
        else:
            return self.get_height(from_pos) - 1 <= self.get_height(to_pos)

    def get_visited(self, pos: Position) -> None:
        row, col = pos.as_tuple
        return self.visitedmap[row][col]

    def set_as_visited(self, pos: Position) -> None:
        row, col = pos.as_tuple
        self.visitedmap[row][col] = True

    def is_unvisited(self, pos: Position) -> bool:
        row, col = pos.as_tuple
        return not self.visitedmap[row][col]

    def get_distance(self, pos: Position) -> float:
        row, col = pos.as_tuple
        return self.distancemap[row][col]

    def set_distance(self, pos: Position, value) -> None:
        row, col = pos.as_tuple
        self.distancemap[row][col] = value

    def update_distance(self, pos: Position, value) -> None:
        current_value = self.get_distance(pos)
        if value < current_value:
            self.set_distance(pos, value)

    @property
    def shape(self):
        return len(self.heightmap), len(self.heightmap[0])

    def unvisited_neighbors(self, pos: Position):

        unvisited_neighbors = []

        row, col = pos.as_tuple
        max_row_plus1, max_col_plus1 = self.shape

        for candidate_row, candidate_col in [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]:
            if (0 <= candidate_row < max_row_plus1) & (
                0 <= candidate_col < max_col_plus1
            ):
                candidate = Position(candidate_row, candidate_col)
                if self.is_unvisited(candidate) & self.is_accessible(pos, candidate):
                    unvisited_neighbors.append(candidate)

        return unvisited_neighbors

    def calculate_distances(self):

        while self.to_be_evaluated:

            current_pos = self.to_be_evaluated.pop(0)

            if self.is_unvisited(current_pos):

                current_dist = self.get_distance(current_pos)

                unvisited_neighbors = self.unvisited_neighbors(current_pos)

                for unvisited_neighbor in unvisited_neighbors:
                    self.update_distance(unvisited_neighbor, current_dist + 1)
                    self.to_be_evaluated.append(unvisited_neighbor)

                self.set_as_visited(current_pos)


def get_heightmap_startpos_targetpos(
    file: str,
) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:

    heightmap = []

    for row, data in enumerate(get_data(file)):

        startpos_col = data.find("S")
        if startpos_col != -1:
            startpos = Position(row, startpos_col)

        targetpos_column = data.find("E")
        if targetpos_column != -1:
            targetpos = Position(row, targetpos_column)

        heightmap_row_alphabet = data.replace("S", "a").replace("E", "z")
        heightmap_row = [ord(char) - 96 for char in heightmap_row_alphabet]

        heightmap.append(heightmap_row)

    return heightmap, startpos, targetpos


def part_1(file: str):

    heightmap, startpos, targetpos = get_heightmap_startpos_targetpos(file)

    map = DijkstraMap(heightmap, startpos)

    map.calculate_distances()

    print("Part 1:", int(map.get_distance(targetpos)))


def part_2(file: str):

    heightmap, _, targetpos = get_heightmap_startpos_targetpos(file)

    map = DijkstraMap(heightmap, targetpos, downhill=True)

    map.calculate_distances()

    min_scenic_len = inf

    for row, row_list in enumerate(map.distancemap):
        for col, dist in enumerate(row_list):
            if map.heightmap[row][col] == 1:
                if dist < min_scenic_len:
                    min_scenic_len = int(dist)

    print("Part 2:", min_scenic_len)


def main(file: str):
    part_1(file)
    part_2(file)


if __name__ == "__main__":
    main("data.txt")
