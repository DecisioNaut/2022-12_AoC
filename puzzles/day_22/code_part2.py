import re


def get_raw_data(file_path: str) -> list[str]:
    raw_data = []
    with open(file_path, mode="r") as f:
        for line in f.readlines():
            raw_data.append(line)
    return raw_data


def get_directions(raw_data: list[str]) -> list[tuple[str, int | str]]:
    directions = []
    raw_directions = re.findall(r"(\d+|R|L)", raw_data[-1].strip())
    for raw_direction in raw_directions:
        try:
            directions.append(("move", int(raw_direction)))
        except ValueError as e:
            directions.append(("turn", raw_direction))
    return directions


def get_board(raw_data: list[str]) -> list[list[str]]:
    board = []
    raw_board = raw_data[:-2]
    length = max(map(len, raw_board)) - 1
    for row in raw_board:
        stubbed_cols = list(row.replace("\n", ""))
        cols = stubbed_cols + [" " for i in range(length - len(stubbed_cols))]
        board.append(cols)
    return board


def turn_right(dr, dc):
    return dc, -dr


def turn_left(dr, dc):
    return -dc, dr


def turn_around(dr, dc):
    return -dr, -dc


def eval_direction(dr, dc):
    if dc == 1:
        return 0
    elif dr == 1:
        return 1
    elif dc == -1:
        return 2
    elif dr == -1:
        return 3
    else:
        raise ValueError


edge_01 = [(0, c) for c in range(50, 100)]
edge_02 = [(0, c) for c in range(100, 150)]
edge_03 = [(r, 149) for r in range(0, 50)]
edge_04 = [(49, c) for c in range(100, 150)]
edge_05 = [(r, 99) for r in range(50, 100)]
edge_06 = [(r, 99) for r in range(100, 150)]
edge_07 = [(149, c) for c in range(50, 100)]
edge_08 = [(r, 49) for r in range(150, 200)]
edge_09 = [(199, c) for c in range(0, 50)]
edge_10 = [(r, 0) for r in range(150, 200)]
edge_11 = [(r, 0) for r in range(100, 150)]
edge_12 = [(100, c) for c in range(0, 50)]
edge_13 = [(r, 50) for r in range(50, 100)]
edge_14 = [(r, 50) for r in range(0, 50)]


def move_ahead(r, c, dr, dc):
    # edge 01 > edge 10 (turns right)
    if ((r, c) in edge_01) & (dr == -1):
        _r, _c = c + 100, r  # checked
        _dr, _dc = turn_right(dr, dc)
    # edge 02 > edge 09 (keeps ahead)
    elif ((r, c) in edge_02) & (dr == -1):
        _r, _c = r + 199, c - 100  # checked
        _dr, _dc = dr, dc
    # edge 03 > edge 06 (turns around)
    elif ((r, c) in edge_03) & (dc == 1):
        _r, _c = 149 - r, c - 50  # checked
        _dr, _dc = turn_around(dr, dc)
    # edge 04 > edge 05 (turns right)
    elif ((r, c) in edge_04) & (dr == 1):
        _r, _c = c - 50, r + 50  # checked
        _dr, _dc = turn_right(dr, dc)
    # edge 05 > edge 04 (turns left)
    elif ((r, c) in edge_05) & (dc == 1):
        _r, _c = c - 50, r + 50  # checked
        _dr, _dc = turn_left(dr, dc)
    # edge 06 > edge 03 (turns around)
    elif ((r, c) in edge_06) & (dc == 1):
        _r, _c = 149 - r, c + 50  # checked
        _dr, _dc = turn_around(dr, dc)
    # edge 07 > edge 08 (turns right)
    elif ((r, c) in edge_07) & (dr == 1):
        _r, _c = c + 100, r - 100  # checked
        _dr, _dc = turn_right(dr, dc)
    # edge 08 > edge 07 (turns left)
    elif ((r, c) in edge_08) & (dc == 1):
        _r, _c = c + 100, r - 100  # checked
        _dr, _dc = turn_left(dr, dc)
    # edge 09 > edge 02 (keeps ahead)
    elif ((r, c) in edge_09) & (dr == 1):
        _r, _c = r - 199, c + 100  # checked
        _dr, _dc = dr, dc
    # edge 10 > edge 01 (turns left)
    elif ((r, c) in edge_10) & (dc == -1):
        _r, _c = c, r - 100  # checked
        _dr, _dc = turn_left(dr, dc)
    # edge 11 > edge 14 (turns around)
    elif ((r, c) in edge_11) & (dc == -1):
        _r, _c = 149 - r, c + 50  # checked
        _dr, _dc = turn_around(dr, dc)
    # edge 12 > edge 13 (turns right)
    elif ((r, c) in edge_12) & (dr == -1):
        _r, _c = c + 50, r - 50  # checked
        _dr, _dc = turn_right(dr, dc)
    # edge 13 > edge 12 (turns left)
    elif ((r, c) in edge_13) & (dc == -1):
        _r, _c = c + 50, r - 50  # checked
        _dr, _dc = turn_left(dr, dc)
    # edge 14 > edge 11 (turns around)
    elif ((r, c) in edge_14) & (dc == -1):
        _r, _c = 149 - r, c - 50  # checked
        _dr, _dc = turn_around(dr, dc)
    else:
        _r, _c = r + dr, c + dc
        _dr, _dc = dr, dc
    return _r, _c, _dr, _dc


raw_data = get_raw_data("./puzzles/day_22/data.txt")

board = get_board(raw_data)
directions = get_directions(raw_data)

r, c, dr, dc = 0, 50, 0, 1

for type, order in directions:
    if type == "turn":
        if order == "R":
            dr, dc = turn_right(dr, dc)
        elif order == "L":
            dr, dc = turn_left(dr, dc)
    else:
        assert isinstance(order, int)
        for t in range(order):
            _r, _c, _dr, _dc = move_ahead(r, c, dr, dc)
            if board[_r][_c] == ".":
                r, c, dr, dc = _r, _c, _dr, _dc
            elif board[_r][_c] == "#":
                break

result = 1000 * (r + 1) + 4 * (c + 1) + eval_direction(dr, dc)

print(result)
