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
        return time * self.register[time - 1]


class CRT:
    def __init__(self):
        self.screen = [["." for i in range(40)] for j in range(6)]
        self.beam = ["." if not (j in [1 - 1, 1, 1 + 1]) else "#" for j in range(40)]

    def update_beam(self, i):
        self.beam = ["." if not (j in [i - 1, i, i + 1]) else "#" for j in range(40)]

    def update_screen(self, i):
        column = i % 40
        row = i // 40
        self.screen[row][column] = self.beam[column]

    def show(self):
        for row in self.screen:
            print("".join(row))


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

    crt = CRT()

    for time, cpu in enumerate(device.register[:-1]):
        crt.update_beam(cpu)
        crt.update_screen(time)

    crt.show()


if __name__ == "__main__":
    main()
