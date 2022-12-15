def get_data(file: str):
    with open("./puzzles/day_15/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def part_1(file: str):
    print(
        "Part 1:",
    )


def part_2(file: str):
    print(
        "Part 2:",
    )


def main(file: str):
    part_1(file)
    part_2(file)


if __name__ == "__main__":
    main("example.txt")
