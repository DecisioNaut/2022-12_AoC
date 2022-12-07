def get_data(file: str):

    levels = []
    directions = []

    with open("./puzzles/day_05/" + file, mode="r") as in_file:

        for line in in_file.readlines():

            # Extract starting position data
            # (needs later mangling)
            if "[" in line:
                amended_line = line[:-1] + " "
                lenght = len(amended_line)
                level = []
                for i in range(lenght)[1::4]:
                    level.append(amended_line[i])
                levels.append(level)

            # Extract directions data
            elif "move" in line:
                amended_line = (
                    line.strip()
                    .replace("move ", "")
                    .replace(" from ", ", ")
                    .replace(" to ", ", ")
                )
                direction = dict(
                    zip(
                        ["move", "frm", "to"],
                        [int(item) for item in amended_line.split(", ")],
                    )
                )
                directions.append(direction)
            else:
                pass

    # Mangling starting position data
    levels = list(reversed(levels))
    num_stacks = len(levels[0])
    stacks = [["_"] for i in range(num_stacks)]
    for level in levels:
        for i, item in enumerate(level):
            if item != " ":
                stacks[i].append(item)

    return stacks, directions


class Ship:
    def __init__(self, stacks, directions):
        self.stacks = stacks
        self.directions = directions

    def execute_direction(self, move: int, frm: int, to: int) -> None:
        frm_stack = self.stacks[frm - 1]
        to_stack = self.stacks[to - 1]

        crates_to_move = list(reversed(frm_stack[-move:]))
        new_frm_stack = frm_stack[:-move]
        new_to_stack = to_stack + crates_to_move

        self.stacks[frm - 1] = new_frm_stack
        self.stacks[to - 1] = new_to_stack

    def execute_all(self):
        for direction in self.directions:
            self.execute_direction(**direction)

    def tops(self):
        return "".join([stack[-1] for stack in self.stacks]).replace("_", " ")


class NewShip:
    def __init__(self, stacks, directions):
        self.stacks = stacks
        self.directions = directions

    def execute_direction(self, move: int, frm: int, to: int) -> None:
        frm_stack = self.stacks[frm - 1]
        to_stack = self.stacks[to - 1]

        # New ship doesn't reverse!
        crates_to_move = frm_stack[-move:]
        new_frm_stack = frm_stack[:-move]
        new_to_stack = to_stack + crates_to_move

        self.stacks[frm - 1] = new_frm_stack
        self.stacks[to - 1] = new_to_stack

    def execute_all(self):
        for direction in self.directions:
            self.execute_direction(**direction)

    def tops(self):
        return "".join([stack[-1] for stack in self.stacks]).replace("_", " ")


def main():

    file = "part_1_data.txt"

    # Part 1
    stacks, directions = get_data(file)
    ship = Ship(stacks=stacks, directions=directions)
    ship.execute_all()
    print("Part 1:", ship.tops())

    # Part 2
    stacks, directions = get_data(file)
    print(stacks)
    newship = NewShip(stacks=stacks, directions=directions)
    newship.execute_all()
    print("Part 2:", newship.tops())


if __name__ == "__main__":
    main()
