from typing import List, Tuple


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
        return f"[{self.row}, [{self.col}]]"


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
        self, start_pos: Position, target_pos: Position, height_map: HeightMap
    ) -> None:
        self._start_pos = start_pos
        self._target_pos = target_pos
        self._height_map = height_map
        self._visited_map = VisitedMap(height_map=height_map, start_pos=start_pos)

        self.current_pos = start_pos

    def _neighbor_positions(
        self, current_pos: Position
    ) -> Tuple[Position, Position, Position, Position]:
        current_row = current_pos.row
        current_col = current_pos.col
        max_row, max_col = self._map.shape
        up = Position(max(current_row - 1, 0), current_col)
        down = Position(min(current_row + 1, max_row - 1), current_col)
        left = Position(current_row, max(current_col - 1, 0))
        right = Position(current_row, min(current_col + 1, max_col - 1))
        return up, down, left, right

    def _possible_next(self, current_pos: Position):
        neighbor_positions = self._neighbor_positions(current_pos)


def part_1(file: str):

    height_map_data, start_pos, target_pos = get_height_map_start_pos_target_pos(file)
    start_pos = Position(*start_pos)
    target_pos = Position(*target_pos)
    height_map = HeightMap(height_map_data=height_map_data)
    visited_map = VisitedMap(height_map=height_map, start_pos=start_pos)

    print(visited_map.not_visited(start_pos))
    print(height_map.height_difference(start_pos, target_pos))


def part_2(file: str):
    print(
        "Part 2:",
    )


def main(file: str):
    part_1(file)
    part_2(file)


if __name__ == "__main__":
    main("example.txt")
