def get_data(file: str):
    with open("./puzzles/day_10/" + file, mode="r") as in_file:
        for line in in_file.readlines():
            yield line.strip()


class Device:
    def __init__(self, instructions):
        # Initial conditions
        self.clock = 0
        self.cpu = 1
        self.register = [self.cpu]
        # Instructions
        self.instructions = instructions

    def noop(self):
        self.clock += 1
        self.register.append(self.cpu)

    def addx(self, value):
        value = int(value)
        self.clock += 1
        self.register.append(self.cpu)
        self.clock += 1
        self.cpu += value
        self.register.append(self.cpu)

    def run(self):
        for instruction in self.instructions:
            if instruction[0] == "noop":
                self.noop()
            else:
                self.addx(value=instruction[1])

    def signal_strength_at(self, time):
        # print(time, self.register[time - 1], time * self.register[time - 1])
        return time * self.register[time - 1]


def main():

    instructions = []
    for data in get_data("data.txt"):
        instructions.append(data.split(" "))

    device = Device(instructions=instructions)
    device.run()

    times = [20, 60, 100, 140, 180, 220]
    signals = []

    for time in times:
        signals.append(device.signal_strength_at(time))

    print("Part 1:", sum(signals))


if __name__ == "__main__":
    main()
