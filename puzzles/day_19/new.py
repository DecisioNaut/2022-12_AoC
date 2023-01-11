def dfs(bp, maxspend, cache, time, bots, amts):

    if time == 0:
        return amts[3]

    key = tuple([*bots, *amts])
    if key in cache:
        return cache[key]

    maxval = amts[3] + bots[3] * time

    for bot, recipe in enumerate(bp):

        if bot != 3 and bots[bot] >= maxspend[bot]:
            continue

        wait = 0

        for bot_type, amt in enumerate(recipe):

            if amt == 0:
                continue

            if bots[bot_type] == 0:
                break

            wait = max(wait, -(-(amt - amts[bot_type]) // bots[bot_type]))

        else:

            remtime = time - wait - 1
            if remtime <= 0:
                continue

            next_amts = [x + y * (wait + 1) for x, y in zip(amts, bots)]
            for bot_type, amt in enumerate(recipe):
                next_amts[bot_type] -= amt
            for i in range(3):
                next_amts[i] = min(next_amts[i], maxspend[i] * remtime)

            next_bots = bots[:]
            next_bots[bot] += 1

            maxval = max(
                maxval, dfs(bp, maxspend, cache, remtime, next_bots, next_amts)
            )

    cache[key] = maxval

    return maxval


# bp = [[(0, 4)], [(0, 2)], [(0, 3), (1, 14)], [(0, 2), (2, 7)]]
bp = [[4, 0, 0], [2, 0, 0], [3, 14, 0], [2, 0, 7]]
maxspend = [4, 14, 7]

print(dfs(bp, maxspend, {}, 24, [1, 0, 0, 0], [0, 0, 0, 0]))
