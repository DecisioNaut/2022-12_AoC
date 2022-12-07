from typing import List, Tuple


def read_data(file: str) -> List[str]:
    raw_rucksacks = []
    with open("./puzzles/day_03/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            raw_rucksacks.append(line.strip())
    return raw_rucksacks


def get_compartments(raw_rucksacks: List[str]) -> List[Tuple[str, str]]:
    rucksacks_with_compartment = []
    for raw_rucksack in raw_rucksacks:
        lenght = len(raw_rucksack)
        assert lenght % 2 == 0

        compartment_1, compartment_2 = (
            raw_rucksack[0 : int(lenght / 2)],
            raw_rucksack[-int(lenght / 2) :],
        )

        rucksacks_with_compartment.append((compartment_1, compartment_2))
    return rucksacks_with_compartment


def get_overlap_1(rucksacks_with_compartment: List[Tuple[str, str]]):
    overlap = []
    for rucksack_with_compartment in rucksacks_with_compartment:
        overlap.append(
            list(
                set.intersection(
                    set(rucksack_with_compartment[0]), set(rucksack_with_compartment[1])
                )
            )[0]
        )
    return overlap


def get_combined_rucksacks(raw_rucksacks: List[str]) -> List[List[str]]:
    combined_rucksacks = []
    assert len(raw_rucksacks) % 3 == 0

    for i in range(int(len(raw_rucksacks) / 3)):
        combined_rucksacks.append(
            [raw_rucksacks[3 * i], raw_rucksacks[3 * i + 1], raw_rucksacks[3 * i + 2]]
        )

    return combined_rucksacks


def get_overlap_2(combined_rucksacks: List[Tuple[str, str]]):
    overlap = []
    for combined_rucksack in combined_rucksacks:
        overlap.append(
            list(
                set(combined_rucksack[0])
                .intersection(set(combined_rucksack[1]))
                .intersection(set(combined_rucksack[2]))
            )[0]
        )
    return overlap


def priority(letter: str) -> int:
    assert isinstance(letter, str)
    assert len(letter) == 1
    if letter.lower() == letter:
        return ord(letter) - 96
    else:
        return ord(letter) - 64 + 26


def main():

    raw_rucksacks = read_data("part_1_data.txt")

    # Part 1
    rucksacks_with_compartments = get_compartments(raw_rucksacks)
    overlap_1 = get_overlap_1(rucksacks_with_compartments)
    print("total priority part 1", sum([priority(item) for item in overlap_1]))

    # Part 2
    combined_rucksacks = get_combined_rucksacks(raw_rucksacks)
    print(combined_rucksacks[1])
    overlap_2 = get_overlap_2(combined_rucksacks)
    print("total priority part 2", sum([priority(item) for item in overlap_2]))


if __name__ == "__main__":
    main()
