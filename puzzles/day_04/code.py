from typing import List, Tuple, Set


def get_data(file: str) -> List[Tuple[Set[int], Set[int]]]:
    pairs = []
    with open("./puzzles/day_04/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            raw_pairs = line.strip().split(",")
            assert len(raw_pairs) == 2
            raw_left = raw_pairs[0].split("-")
            raw_left_start, raw_left_end = int(raw_left[0]), int(raw_left[1])
            left = set(range(raw_left_start, raw_left_end + 1))
            raw_right = raw_pairs[1].split("-")
            raw_right_start, raw_right_end = int(raw_right[0]), int(raw_right[1])
            right = set(range(raw_right_start, raw_right_end + 1))
            pairs.append((left, right))
    return pairs


def one_fully_contains(left: Set[int], right: Set[int]) -> bool:
    return left.issubset(right) or right.issubset(left)


def both_overlap(left: Set[int], right: Set[int]) -> bool:
    return left.intersection(right) != set()


def main():
    pairs = get_data("part_1_data.txt")
    print("Part 1:", sum([one_fully_contains(pair[0], pair[1]) for pair in pairs]))
    print("Part 2:", sum([both_overlap(pair[0], pair[1]) for pair in pairs]))


if __name__ == "__main__":
    main()
