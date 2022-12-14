from collections import deque
from operator import add, sub, mul, floordiv
from typing import List


def get_data(file: str) -> str:
    with open("./puzzles/day_11/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def translate_items(items_str: str) -> deque:

    items_str_list = items_str.replace("Starting items: ", "").split(", ")
    items = deque([int(item) for item in items_str_list])

    return items


def translate_operation(operation_str: str):

    operator_str, right_str = operation_str.replace("Operation: new = old", "").split()

    match operator_str:
        case "+":
            operator = add
        case "-":
            operator = sub
        case "*":
            operator = mul
        case "/":
            operator = floordiv

    match right_str:
        case "old":
            return lambda x: operator(x, x)
        case _:
            return lambda x: operator(x, int(right_str))


def translate_test(test_str: str) -> int:
    return int(test_str.replace("Test: divisible by ", ""))


def translate_if_true(if_true_str: str) -> int:
    return int(if_true_str.replace("If true: throw to monkey ", ""))


def translate_if_false(if_false_str: str) -> int:
    return int(if_false_str.replace("If false: throw to monkey ", ""))


def make_test_operation(test: int, if_true: int, if_false: int):
    def test_operation(num):
        return if_true if (num % test == 0) else if_false

    return test_operation


class Monkey:
    def __init__(self, items, change_worry, throw_to, calm_down=True):
        self._inspection_count: int = 0
        self.items: deque = items
        self.change_worry = change_worry
        self.throw_to = throw_to
        self.calm_down = calm_down
        self.contain_worry_level = None

    @property
    def num_items(self):
        return len(self.items)

    @property
    def inspection_count(self):
        return self._inspection_count

    def throw_item(self):
        item = self.items.popleft()
        item_changed_worry = self.change_worry(item)
        item_with_relief = floordiv(item_changed_worry, 3 if self.calm_down else 1)
        throw_to = self.throw_to(item_with_relief)
        self._inspection_count += 1
        return item_with_relief, throw_to

    def catch_item(self, item):
        if self.contain_worry_level:
            item = item % self.contain_worry_level
        self.items.append(item)


def make_monkeys(file: str, calm_down=True) -> List[Monkey]:

    monkeys = []
    contain_worry_level = 1

    for line_num, line_str in enumerate(get_data(file)):

        mod_line_num = line_num % 7

        if mod_line_num in [0, 6]:
            pass

        elif mod_line_num == 1:
            items = translate_items(line_str)

        elif mod_line_num == 2:
            change_worry = translate_operation(line_str)

        elif mod_line_num == 3:
            test = translate_test(line_str)
            contain_worry_level *= test

        elif mod_line_num == 4:
            if_true = translate_if_true(line_str)

        elif mod_line_num == 5:
            if_false = translate_if_false(line_str)
            throw_to = make_test_operation(test, if_true, if_false)
            monkey = Monkey(items, change_worry, throw_to, calm_down=calm_down)
            monkeys.append(monkey)

    for monkey in monkeys:
        monkey.contain_worry_level = contain_worry_level

    return monkeys


def part_1():

    monkeys = make_monkeys("data.txt")

    for i in range(20):
        for monkey in monkeys:
            for j in range(monkey.num_items):
                item, throw_to = monkey.throw_item()
                monkeys[throw_to].catch_item(item)

    inspection_counts = []

    for num, monkey in enumerate(monkeys):
        inspection_counts.append(monkey.inspection_count)

    print("Part 1:", mul(*list(reversed(sorted(inspection_counts)))[:2]))


def part_2():

    monkeys = make_monkeys("data.txt", calm_down=False)

    for i in range(10_000):
        for monkey in monkeys:
            for j in range(monkey.num_items):
                item, throw_to = monkey.throw_item()
                monkeys[throw_to].catch_item(item)

    inspection_counts = []

    for num, monkey in enumerate(monkeys):
        inspection_counts.append(monkey.inspection_count)

    print("Part 2:", mul(*list(reversed(sorted(inspection_counts)))[:2]))


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
