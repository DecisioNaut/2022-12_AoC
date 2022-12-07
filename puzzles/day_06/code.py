def get_data(file: str):
    with open("./puzzles/day_06/" + file, mode="r") as in_file:
        signal = in_file.readline()
    return signal


def main():
    signal = get_data("part_1_data_example.txt")
    print(signal)


if __name__ == "__main__":
    main()
