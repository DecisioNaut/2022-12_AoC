import re


def maximize_geodes(blueprint, max_robots, robots, materials, t, cache):

    if t == 0:
        return materials[3]

    key = tuple([*robots, *materials])
    if key in cache:
        return cache[key]

    maxval = materials[3] + robots[3] * t

    for robot, recipe in enumerate(blueprint):

        if robot != 3 and robots[robot] >= max_robots[robot]:
            continue

        wait = 0

        for material, amount in enumerate(recipe):

            if amount == 0:
                continue

            if robots[material] == 0:
                break

            wait = max(wait, -(-(amount - materials[material]) // robots[material]))

        else:

            t_remain = t - wait - 1
            if t_remain <= 0:
                continue

            next_materials = [x + y * (wait + 1) for x, y in zip(materials, robots)]
            for material, amount in enumerate(recipe):
                next_materials[material] -= amount
                next_materials[material] = min(
                    next_materials[material], max_robots[material] * t_remain
                )

            next_robots = robots[:]
            next_robots[robot] += 1

            maxval = max(
                maxval,
                maximize_geodes(
                    blueprint, max_robots, next_robots, next_materials, t_remain, cache
                ),
            )

    cache[key] = maxval

    return maxval


def get_blueprints():
    blueprints = []
    maxes_robots = []
    with open("./puzzles/day_19/data.txt", mode="r") as f:
        for num, line in enumerate(f.readlines()):

            if num >= 3:
                break

            ore_ore, cly_ore, obs_ore, obs_cly, ged_ore, ged_obs = map(
                int, re.findall("(\d+)", line.split(":")[1][:-1])
            )

            blueprint = [
                [ore_ore, 0, 0],
                [cly_ore, 0, 0],
                [obs_ore, obs_cly, 0],
                [ged_ore, 0, ged_obs],
            ]
            max_robots = [
                max(recipe[robot] for recipe in blueprint) for robot in range(3)
            ]

            blueprints.append(blueprint)
            maxes_robots.append(max_robots)

    return blueprints, maxes_robots


def part2():
    result = 1
    blueprints, maxes_robots = get_blueprints()
    for blueprint, max_robots in zip(blueprints, maxes_robots):
        result *= maximize_geodes(
            blueprint, max_robots, [1, 0, 0, 0], [0, 0, 0, 0], 32, {}
        )
    print("Part 2:", result)


def main():
    part2()


if __name__ == "__main__":
    main()
