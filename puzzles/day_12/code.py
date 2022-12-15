from __future__ import annotations
from typing import List, Tuple, Optional


def get_data(file: str) -> str:
    with open("./puzzles/day_12/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def get_height_map_start_pos_target_pos(
    file: str,
) -> Tuple[List[List[int]], List[int], List[int]]:

    height_map = []

    for row_index, data in enumerate(get_data(file)):

        start_column = data.find("S")
        if start_column != -1:
            start_pos = [row_index, start_column]

        target_pos_column = data.find("E")
        if target_pos_column != -1:
            target_pos = [row_index, target_pos_column]

        height_map_row_alphabet = data.replace("S", "a").replace("E", "z")
        height_map_row = [ord(char) - 96 for char in height_map_row_alphabet]

        height_map.append(height_map_row)

    return height_map, start_pos, target_pos


class Position:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

    def __repr__(self) -> str:
        return f"[{self.row}, {self.col}]"

    def __eq__(self, other: Position) -> bool:
        return (self.row == other.row) & (self.col == other.col)

    def __ne__(self, other: Position) -> bool:
        return (self.row != other.row) | (self.col != other.col)


class HeightMap:
    def __init__(self, height_map_data: List[List[int]]) -> None:
        self._height_map_data = height_map_data

    @property
    def shape(self) -> Tuple[int, int]:
        return len(self._height_map_data), len(self._height_map_data[0])

    def __repr__(self) -> str:
        height_map_string = f"\n".join(
            ["".join([chr(item + 96) for item in row]) for row in self._height_map_data]
        )
        return height_map_string

    def __getitem__(self, index) -> List[int]:
        return self._height_map_data[index]

    def height(self, pos: Position):
        return self._height_map_data[pos.row][pos.col]

    def height_difference(self, current_pos: Position, next_pos: Position) -> int:
        current_height = self.height(current_pos)
        next_height = self.height(next_pos)
        return next_height - current_height


""" 
class VisitedMap:
    def __init__(self, height_map: HeightMap, start_pos: Position) -> None:
        visited_map_data = [[False for item in row] for row in height_map]
        visited_map_data[start_pos.row][start_pos.col] = True
        self._visited_map_data = visited_map_data

    def __repr__(self) -> str:
        visited_map_str = f"\n".join(
            [
                "".join([("1" if item else "0") for item in row])
                for row in self._visited_map_data
            ]
        )
        return visited_map_str

    def __getitem__(self, index) -> List[bool]:
        return self._visited_map_data[index]

    def update(self, pos: Position) -> None:
        self._visited_map_data[pos.row][pos.col] = True

    def visited(self, pos: Position) -> bool:
        return self._visited_map_data[pos.row][pos.col]

    def not_visited(self, pos: Position) -> None:
        return not self.visited(pos)

    @property
    def num_visited(self):
        return sum([sum(row) for row in self._visited_map_data])


class Path:
    def __init__(
        self,
        start_pos: Position,
        target_pos: Position,
        height_map: HeightMap,
        visited_map: Optional[VisitedMap] = None,
    ) -> None:

        self._start_pos = start_pos
        self._target_pos = target_pos
        self._height_map = height_map

        if not visited_map:
            self._visited_map = VisitedMap(height_map=height_map, start_pos=start_pos)
        else:
            self._visited_map = visited_map

        self.current_pos = start_pos

    def update(self, pos: Position) -> None:
        self._visited_map.update(pos)

    def _neighbor_positions(
        self, current_pos: Position
    ) -> Tuple[Position, Position, Position, Position]:
        current_row = current_pos.row
        current_col = current_pos.col
        max_row, max_col = self._height_map.shape
        up = Position(max(current_row - 1, 0), current_col)
        down = Position(min(current_row + 1, max_row - 1), current_col)
        left = Position(current_row, max(current_col - 1, 0))
        right = Position(current_row, min(current_col + 1, max_col - 1))
        return up, down, left, right

    def _possible_nexts(self, current_pos: Position):
        neighbors = self._neighbor_positions(current_pos)
        unvisited_neighbors = [
            neighbor
            for neighbor in neighbors
            if self._visited_map.not_visited(neighbor)
        ]
        possible_nexts = [
            unvisited_neighbor
            for unvisited_neighbor in unvisited_neighbors
            if self._height_map.height_difference(current_pos, unvisited_neighbor) <= 1
        ]
        return possible_nexts

    def get_next(self) -> List[Path]:

        possible_nexts = self._possible_nexts(self.current_pos)

        if possible_nexts != []:

            next_paths = []

            for possible_next in possible_nexts:

                start_pos = self._start_pos
                target_pos = self._target_pos
                height_map = self._height_map
                visited_map = self._visited_map

                next_path = Path(
                    start_pos=start_pos,
                    target_pos=target_pos,
                    height_map=height_map,
                    visited_map=visited_map,
                )
                next_path.update(possible_next)

                next_paths.append(next_path)

        return next_paths
 """


class Path:
    def __init__(
        self, start_pos: Position, target_pos: Position, height_map: HeightMap
    ) -> None:

        self.current_pos = start_pos
        self.target_pos = target_pos

        self.height_map = height_map

        max_row_plus_1, max_col_plus_1 = height_map.shape
        self.max_row = max_row_plus_1 - 1
        self.max_col = max_col_plus_1 - 1

        self.path = [start_pos]

    def __repr__(self) -> str:
        return repr(self.path)

    __str__ = __repr__

    @property
    def at_target(self):
        return self.current_pos == self.target_pos

    @property
    def stuck(self):
        return self.available_neighbors == []

    @property
    def done(self):
        return self.at_target | self.stuck

    def __add__(self, next_position: Position):
        assert next_position in self.available_neighbors
        assert not self.done
        self.current_pos = next_position
        self.path.append(next_position)

    def visited(self, pos: Position) -> bool:
        return True if pos in self.path else False

    @property
    def current_neighbors(self) -> List[Position]:

        if self.current_pos != self.target_pos:
            cur_row = self.current_pos.row
            cur_col = self.current_pos.col

            max_row = self.max_row
            max_col = self.max_col

            interm_neighbors = []

            interm_neighbors.append(Position(max(cur_row - 1, 0), cur_col))
            interm_neighbors.append(Position(min(cur_row + 1, max_row), cur_col))

            interm_neighbors.append(Position(cur_row, max(cur_col - 1, 0)))
            interm_neighbors.append(Position(cur_row, min(cur_col + 1, max_col)))

            current_neighbors = [
                interm_neighbor
                for interm_neighbor in interm_neighbors
                if interm_neighbor != self.current_pos
            ]

            return current_neighbors

        else:

            return []

    @property
    def unvisited_neighbors(self) -> Optional[List[Position]]:

        current_neighbors = self.current_neighbors

        unvisited_neighbors = [
            current_neighbor
            for current_neighbor in current_neighbors
            if not (self.visited(current_neighbor))
        ]

        return unvisited_neighbors

    @property
    def available_neighbors(self) -> List[Position]:

        unvisited_neighbors = self.unvisited_neighbors

        available_neighbors = [
            unvisited_neighbor
            for unvisited_neighbor in unvisited_neighbors
            if self.height_map.height_difference(self.current_pos, unvisited_neighbor)
            <= 1
        ]

        return available_neighbors

    def make_path(self):

        while self.available_neighbors:
            self + self.available_neighbors[0]


def part_1(file: str):

    height_map_data, start_pos, target_pos = get_height_map_start_pos_target_pos(file)

    start_pos = Position(*start_pos)
    target_pos = Position(*target_pos)
    height_map = HeightMap(height_map_data=height_map_data)

    path = Path(start_pos=start_pos, target_pos=target_pos, height_map=height_map)

    path.make_path()

    print(len(path.path))


def part_2(file: str):
    print(
        "Part 2:",
    )


def main(file: str):
    part_1(file)
    part_2(file)


if __name__ == "__main__":
    main("example.txt")
