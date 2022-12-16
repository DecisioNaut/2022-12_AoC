from __future__ import annotations
from typing import List, Tuple
from math import inf


def get_data(file: str) -> str:
    with open("./puzzles/day_12/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def get_heightmap_startpos_targetpos(
    file: str,
) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:

    heightmap = []

    for row, data in enumerate(get_data(file)):

        startpos_col = data.find("S")
        if startpos_col != -1:
            startpos = (row, startpos_col)

        targetpos_column = data.find("E")
        if targetpos_column != -1:
            targetpos = (row, targetpos_column)

        heightmap_row_alphabet = data.replace("S", "a").replace("E", "z")
        heightmap_row = [ord(char) - 96 for char in heightmap_row_alphabet]

        heightmap.append(heightmap_row)

    return heightmap, startpos, targetpos


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
        self,
        heightmap: List[List[int]],
        startpos: Tuple[int, int],
        targetpos: Tuple[int, int],
    ) -> None:

        # Setting up basic data
        self.heightmap = heightmap
        self.targetpos = Position(*targetpos)

        # 1. Mark all nodes as unvisited
        self.visitedmap = [[False for col in row] for row in heightmap]

        # 2. Assign every node a tentative distance inf, except startpos where it's 0
        self.distancemap = [[inf for col in row] for row in heightmap]
        self.distancemap[startpos[0]][startpos[1]] = 0

        # Setting up a deque for positions to be evaluated
        self.to_be_evaluated = [Position(*startpos)]

    def is_unvisited(self, pos: Position) -> bool:
        row, col = pos.as_tuple
        return not self.visitedmap[row][col]

    def is_accessible(self, from_pos: Position, to_pos: Position) -> bool:
        from_row, from_col = from_pos.as_tuple
        to_row, to_col = to_pos.as_tuple
        return self.heightmap[to_row][to_col] - 1 <= self.heightmap[from_row][from_col]

    def get_distance(self, pos: Position) -> float:
        row, col = pos.as_tuple
        return self.distancemap[row][col]

    def set_distance(self, pos: Position, value) -> None:
        row, col = pos.as_tuple
        self.distancemap[row][col] = value

    def update_distance(self, pos: Position, value) -> None:
        row, col = pos.as_tuple
        current_value = self.distancemap[row][col]
        if value < current_value:
            self.distancemap[row][col] = value

    def set_visited(self, pos: Position) -> None:
        row, col = pos.as_tuple
        self.visitedmap[row][col] = True

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
            current_dist = self.get_distance(current_pos)

            unvisited_neighbors = self.unvisited_neighbors(current_pos)

            for unvisited_neighbor in unvisited_neighbors:
                self.update_distance(unvisited_neighbor, current_dist + 1)
                self.to_be_evaluated.append(unvisited_neighbor)

            self.set_visited(current_pos)


def part_1(file: str):

    map = DijkstraMap(*get_heightmap_startpos_targetpos(file))

    map.calculate_distances()
    print(map.get_distance(map.targetpos))

    print(
        "Part 1:",
    )


def part_2(file: str):
    print(
        "Part 2:",
    )


def main(file: str):
    part_1(file)
    part_2(file)


if __name__ == "__main__":
    main("data.txt")
