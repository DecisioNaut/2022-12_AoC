def get_data(file: str) -> str:
    with open("/puzzles/day_14/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


def main():
    ...


if __name__ == "__main__":
    main()
