def dfs(blueprint, max_robots, robots, materials, t, cache):

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
                dfs(
                    blueprint, max_robots, next_robots, next_materials, t_remain, cache
                ),
            )

    cache[key] = maxval

    return maxval


blueprint = [[4, 0, 0], [2, 0, 0], [3, 14, 0], [2, 0, 7]]
max_robots = [max(recipe[robot] for recipe in blueprint) for robot in range(3)]
print(max_robots)

print(dfs(blueprint, max_robots, [1, 0, 0, 0], [0, 0, 0, 0], 24, {}))
