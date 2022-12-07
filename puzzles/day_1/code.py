from typing import List

1


def read_elves(file: str) -> List[List[int]]:

    elves = []
    elf = []

    with open("./puzzles/day_1/" + file) as in_file:
        for item in in_file.readlines():
            if item.strip() == "":
                elves.append(elf)
                elf = []
            else:
                elf.append(int(item))

        elves.append(elf)

    return elves


def elves_total_calories(elves: List[List[int]]) -> List[int]:

    total_calories = []

    for elf in elves:
        total_calories.append(sum(elf))

    return total_calories


def main():
    elves = read_elves("part_1_data.txt")
    print("elves", elves)
    total_calories = elves_total_calories(elves)
    print("total_calories", total_calories)

    # Result part 1
    print("max_total_calories", max(total_calories))

    # Result part 2
    print(sum(sorted(total_calories)[-3:]))


if __name__ == "__main__":
    main()
