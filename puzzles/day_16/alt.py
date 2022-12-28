import re
from itertools import product, combinations
from functools import reduce

data = [
    (v, int(f), e.split(", "))
    for v, f, e in re.findall(
        r"([A-Z]{2}).+=(\d+).+es? (.+)", open("./puzzles/day_16/data.txt").read()
    )
]
flow = {v: f for v, f, _ in data}
dist, V = {
    v1: {v2: (0 if v1 == v2 else 1 if v2 in e else 10000) for v2, _, _ in data}
    for v1, _, e in data
}, set(v for v, f, _ in data if f > 0)
for k, i, j in product(dist.keys(), repeat=3):
    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])


def dfs(time, paths, v="AA", visited=frozenset(), pressure=0):
    paths[visited] = max(paths[visited], pressure) if visited in paths else pressure
    for v_next, time_next in [
        (v_next, time_next)
        for v_next in (V - visited)
        if (time_next := time - dist[v][v_next] - 1) > 0
    ]:
        dfs(
            time_next,
            paths,
            v_next,
            visited | {v_next},
            pressure + flow[v_next] * time_next,
        )
    return paths


print(max(dfs(30, {}).values()))
print(
    reduce(
        lambda acc, i: max(acc, i[0][1] + i[1][1])
        if len(i[0][0] & i[1][0]) == 0
        else acc,
        combinations(dfs(26, {}).items(), 2),
        0,
    )
)
