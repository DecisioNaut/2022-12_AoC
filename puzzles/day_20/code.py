from __future__ import annotations

from typing import List, Optional


def get_data(file: str):
    with open("./puzzles/day_20/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def get_initial_state(file: str) -> List[int]:
    initial_state = []
    for data in get_data(file):
        initial_state.append(int(data))
    return initial_state


class LinkValue:
    def __init__(
        self,
        value: int,
        pred: Optional[LinkValue] = None,
        succ: Optional[LinkValue] = None,
    ) -> None:
        self._value = value
        self._pred = pred
        self._succ = succ

    @property
    def value(self):
        return self._value

    def set_pred(self, pred: LinkValue) -> LinkValue:
        self._pred = pred
        return self

    @property
    def pred(self) -> LinkValue:
        return self._pred

    @pred.setter
    def pred(self, other: LinkValue) -> None:
        self._pred = other

    def set_succ(self, succ: LinkValue) -> LinkValue:
        self._succ = succ
        return self

    @property
    def succ(self) -> LinkValue:
        return self._succ

    @succ.setter
    def succ(self, other: LinkValue) -> None:
        self._succ = other

    def __str__(self) -> str:
        return str(self._value)

    def __getitem__(self, ind):
        if ind == 0:
            return self
        elif ind > 0:
            current_pos = self
            for i in range(ind):
                current_pos = current_pos._succ
            return current_pos
        elif ind < 0:
            current_pos = self
            for i in range(-ind):
                current_pos = current_pos._pred
            return current_pos


class CircularLinkedValues:
    def __init__(self, initial_state: List[int]) -> None:

        # Set linked_nums without predecessors and successors
        self._linked_vals: List[LinkValue] = [LinkValue(num) for num in initial_state]

        # Set predecessors for each linked_num
        preds: List[LinkValue] = [self._linked_vals[-1]] + self._linked_vals[:-1]
        self._linked_vals = [
            linked_value.set_pred(pred)
            for linked_value, pred in zip(self._linked_vals, preds)
        ]

        # Set successors for each linked_num
        succs: List[LinkValue] = self._linked_vals[1:] + [self._linked_vals[0]]
        self._linked_vals = [
            linked_value.set_succ(succ)
            for linked_value, succ in zip(self._linked_vals, succs)
        ]

    def __len__(self) -> int:
        return len(self._linked_vals)

    def __getitem__(self, ind):
        return self._linked_vals[ind]

    def move_item_by_places(self, index_of_item: int, places: int):

        item = self._linked_vals[index_of_item]

        if places == 0:
            pass

        elif places == 1:

            # Other items affected
            pred, succ, succsucc = item[-1], item[+1], item[+2]

            # Change of preds and succs of other items affected
            pred.succ = succ
            succ.pred, succ.succ = pred, item
            item.pred, item.succ = succ, succsucc
            succsucc.pred = item

        elif places == -1:

            # Other items affected
            predpred, pred, succ = item[-2], item[-1], item[+1]

            # Change of preds and succs of other items affected
            predpred.succ = item
            item.pred, item.succ = predpred, pred
            pred.pred, pred.succ = item, succ
            succ.pred = item

        elif places > 1:

            # Other items affected
            old_pred, old_succ = item[-1], item[+1]
            new_pred, new_succ = item[places], item[places + 1]

            # Change of old_pred, old_succ preds and succs
            old_pred.succ, old_succ.pred = old_succ, old_pred

            # Change of new_pred, item, new_succ preds and succs
            new_pred.succ, item.pred, item.succ, new_succ.pred = (
                item,
                new_pred,
                new_succ,
                item,
            )

        elif places < -1:

            # Other items affected
            old_pred, old_succ = item[-1], item[+1]
            new_pred, new_succ = item[places - 1], item[places]

            # Change of old_pred, old_succ preds and succs
            old_pred.succ, old_succ.pred = old_succ, old_pred

            # Change of new_pred, item, new_succ preds and succs
            new_pred.succ, item.pred, item.succ, new_succ.pred = (
                item,
                new_pred,
                new_succ,
                item,
            )

    def __str__(self) -> str:
        current_item = self._linked_vals[0]
        string = str(current_item)
        for i in range(1, len(self)):
            current_item = current_item[+1]
            string = string + " > " + str(current_item)
        return string


def part1(file: str) -> None:

    initial_state = get_initial_state(file)
    index_of_zero = initial_state.index(0)

    circular_linked_values = CircularLinkedValues(initial_state)

    for index_of_item, item in enumerate(circular_linked_values):
        places = item.value
        circular_linked_values.move_item_by_places(index_of_item, places)

    result = sum(
        [
            circular_linked_values[index_of_zero][num].value
            for num in [1_000, 2_000, 3_000]
        ]
    )

    print("Part 1:", result)


def part2(file: str) -> None:
    data = get_data(file)
    print(
        "Part 2:",
    )


def main(file: str) -> None:

    part1(file)
    part2(file)


if __name__ == "__main__":
    main("data.txt")
