from __future__ import annotations
from itertools import zip_longest
from functools import total_ordering
from enum import Enum


def get_data(file: str) -> str:
    with open("./puzzles/day_13/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def make_pairs(file: str):

    pairs = dict()

    left, right = None, None

    for line_num, data in enumerate(get_data(file)):
        if line_num % 3 == 0:
            signal = eval(data)
            left = signal
        elif line_num % 3 == 1:
            signal = eval(data)
            right = signal
            pairs[(line_num // 3) + 1] = {"left": left, "right": right}
        else:
            pass

    return pairs


class Result(Enum):
    in_right_order = 1
    not_in_right_order = -1
    undecided = 0


def compare(left, right):

    if isinstance(left, int) & isinstance(right, int):

        if left < right:
            return Result.in_right_order

        elif left > right:
            return Result.not_in_right_order

        else:
            return Result.undecided

    elif isinstance(left, int) & isinstance(right, list):
        return compare([left], right)

    elif isinstance(left, list) & isinstance(right, int):
        return compare(left, [right])

    else:

        zipped = zip_longest(left, right)

        for left_item, right_item in zipped:

            if left_item is None:
                return Result.in_right_order

            elif right_item is None:
                return Result.not_in_right_order

            else:
                result = compare(left_item, right_item)

                if result == Result.in_right_order:
                    return Result.in_right_order

                elif result == Result.not_in_right_order:
                    return Result.not_in_right_order

        return Result.undecided


@total_ordering
class Signal:
    def __init__(self, signal):
        self.signal = signal

    def __eq__(self, other):
        return compare(self.signal, other.signal) == Result.undecided

    def __lt__(self, other):
        return compare(self.signal, other.signal) == Result.in_right_order

    def __str__(self):
        return str(self.signal)

    __repr__ = __str__


def make_signals(file: str):

    signals = list()

    for line_num, data in enumerate(get_data(file)):
        if (line_num % 3 == 0) | (line_num % 3 == 1):
            signal = eval(data)
            signals.append(Signal(signal))
        else:
            pass

    signals.append(Signal(signal=[[2]]))
    signals.append(Signal(signal=[[6]]))

    return signals


def part_1(file: str):

    pairs = make_pairs(file)

    sum_right_order_indices = 0

    for index, pair in pairs.items():
        left = pair["left"]
        right = pair["right"]
        if compare(left, right) == Result.in_right_order:
            sum_right_order_indices += index

    print("Part 1:", sum_right_order_indices)


def part_2(file: str):

    signals = sorted(make_signals(file))

    multiplied_relevant_indices = 1

    for index, signal in enumerate(signals):
        if (signal.signal == [[2]]) | (signal.signal == [[6]]):
            multiplied_relevant_indices *= index + 1

    print("Part 2:", multiplied_relevant_indices)


def main():
    part_1("data.txt")
    part_2("data.txt")


if __name__ == "__main__":
    main()
