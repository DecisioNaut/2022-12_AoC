def get_data(file: str):
    with open("./puzzles/day_06/" + file, mode="r") as in_file:
        signal = in_file.readline()
    return signal


def print_package_marker(signal):
    length = len(signal) - 3
    for i in range(length):
        check_signal = signal[i : i + 4]
        if len(set(check_signal)) == 4:
            print(check_signal, "ends at", i + 4)
            break


def print_message_marker(signal):
    length = len(signal) - 13
    for i in range(length):
        check_signal = signal[i : i + 14]
        if len(set(check_signal)) == 14:
            print(check_signal, "ends at", i + 14)
            break


def main():
    signal = get_data("part_1_data.txt")
    print_package_marker(signal)
    print_message_marker(signal)


if __name__ == "__main__":
    main()
