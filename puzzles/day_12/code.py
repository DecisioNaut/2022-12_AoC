from __future__ import annotations
from typing import List, Tuple, Optional
from copy import deepcopy


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


class Path:
    def __init__(
        self, start_pos: Position, target_pos: Position, height_map: HeightMap
    ) -> None:

        # Meta data
        self.target_pos = target_pos
        self.height_map = height_map
        max_row_plus_1, max_col_plus_1 = height_map.shape
        self.max_row = max_row_plus_1 - 1
        self.max_col = max_col_plus_1 - 1

        # Variable data
        self.current_pos = start_pos
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
        if self.available_neighbors:
            assert next_position in self.available_neighbors
        assert not self.done

        result = deepcopy(self)
        result.current_pos = next_position
        result.path.append(next_position)

        return result

    def __len__(self):
        return len(self.path) - 1

    def visited(self, pos: Position) -> bool:
        return True if pos in self.path else False

    @property
    def current_neighbors(self) -> List[Position]:
        """Function to get all neighbors of current position"""

        if self.current_pos != self.target_pos:

            # Some metadata for later abbrev
            cur_row = self.current_pos.row
            cur_col = self.current_pos.col
            max_row = self.max_row
            max_col = self.max_col

            # initiale list of trimmed neighbors
            interm_neighbors = []

            # up, down trimmed to be on map
            interm_neighbors.append(Position(max(cur_row - 1, 0), cur_col))
            interm_neighbors.append(Position(min(cur_row + 1, max_row), cur_col))

            # left, right trimmed to be on map
            interm_neighbors.append(Position(cur_row, max(cur_col - 1, 0)))
            interm_neighbors.append(Position(cur_row, min(cur_col + 1, max_col)))

            # only trimmed up, down, left, right not being current position
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
        """Function to get all neighbors of current position that have not been visited yet"""

        current_neighbors = self.current_neighbors

        unvisited_neighbors = [
            current_neighbor
            for current_neighbor in current_neighbors
            if not (self.visited(current_neighbor))
        ]

        return unvisited_neighbors

    @property
    def available_neighbors(self) -> List[Position]:
        """Function to get all neighbors that have neither been visited yet, not are more that 1 level up."""

        unvisited_neighbors = self.unvisited_neighbors

        available_neighbors = [
            unvisited_neighbor
            for unvisited_neighbor in unvisited_neighbors
            if self.height_map.height_difference(self.current_pos, unvisited_neighbor)
            <= 1
        ]

        return available_neighbors

    def get_all_paths(self) -> List[Path]:

        available_neighbors = self.available_neighbors

        if available_neighbors == []:

            return [self]

        else:

            result = []

            for available_neighbor in available_neighbors:

                next_path = self + available_neighbor
                result += next_path.get_all_paths()

            return result


def part_1(file: str):

    height_map_data, start_pos, target_pos = get_height_map_start_pos_target_pos(file)

    start_pos = Position(*start_pos)
    target_pos = Position(*target_pos)
    height_map = HeightMap(height_map_data=height_map_data)

    path = Path(start_pos=start_pos, target_pos=target_pos, height_map=height_map)

    all_paths = path.get_all_paths()

    relevant_paths_lengths = [
        len(relevant_path) for relevant_path in all_paths if relevant_path.at_target
    ]

    print("Part 1:", min(relevant_paths_lengths))


def part_2(file: str):
    print(
        "Part 2:",
    )


def main(file: str):
    part_1(file)
    part_2(file)


if __name__ == "__main__":
    main("data.txt")
