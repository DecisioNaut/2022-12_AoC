def dfs(blueprint, max_bots, bots, materials, t, cache):

    if t == 0:
        return materials[3]

    key = tuple([*bots, *materials])
    if key in cache:
        return cache[key]

    maxval = materials[3] + bots[3] * t

    for bot, recipe in enumerate(blueprint):

        if bot != 3 and bots[bot] >= max_bots[bot]:
            continue

        wait = 0

        for material, amt in enumerate(recipe):

            if amt == 0:
                continue

            if bots[material] == 0:
                break

            wait = max(wait, -(-(amt - materials[material]) // bots[material]))

        else:

            t_remain = t - wait - 1
            if t_remain <= 0:
                continue

            next_materials = [x + y * (wait + 1) for x, y in zip(materials, bots)]
            for material, amt in enumerate(recipe):
                next_materials[material] -= amt
                next_materials[material] = min(
                    next_materials[material], max_bots[material] * t_remain
                )
            # for i in range(3):
            #    next_materials[i] = min(next_materials[i], max_bots[i] * t_remain)

            next_bots = bots[:]
            next_bots[bot] += 1

            maxval = max(
                maxval,
                dfs(blueprint, max_bots, next_bots, next_materials, t_remain, cache),
            )

    cache[key] = maxval

    return maxval


blueprint = [[4, 0, 0], [2, 0, 0], [3, 14, 0], [2, 0, 7]]
max_bots = [max(recipe[bot] for recipe in blueprint) for bot in range(3)]
print(max_bots)

print(dfs(blueprint, max_bots, [1, 0, 0, 0], [0, 0, 0, 0], 24, {}))
