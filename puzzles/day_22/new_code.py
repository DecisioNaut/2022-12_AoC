from __future__ import annotations

from typing import Optional


class Quaternion:
    def __init__(self, u, i, j, k) -> None:
        self.u = u
        self.i = i
        self.j = j
        self.k = k

    def __eq__(self, other: Quaternion) -> bool:
        return (
            (self.u == other.u)
            & (self.i == other.i)
            & (self.j == other.j)
            & (self.k == other.k)
        )

    def __mul__(self, other) -> Quaternion:
        u = self.u * other.u - self.i * other.i - self.j * other.j - self.k * other.k
        i = self.u * other.i + self.i * other.u + self.j * other.k - self.k * other.j
        j = self.u * other.j - self.i * other.k + self.j * other.u + self.k * other.i
        k = self.u * other.k + self.i * other.j - self.j * other.i + self.k * other.u
        return Quaternion(u, i, j, k)

    def __repr__(self) -> str:
        return f"Quaternion(u={self.u}, i={self.i}, j={self.j}, k={self.k})"

    def __hash__(self) -> int:
        return hash(("quaternion", self.u, self.i, self.j, self.k))


class Cube:
    def __init__(self, side: int = 1) -> None:
        self.sides = [
            Quaternion(0, 1, 0, 0),
            Quaternion(0, 0, 1, 0),
            Quaternion(0, 0, 0, 1),
            Quaternion(0, 0, 0, -1),
            Quaternion(0, 0, -1, 0),
            Quaternion(0, -1, 0, 0),
        ]
        self.current = self.sides[(side - 1) % 6]

    def __repr__(self) -> str:
        return f"Cube(side={self.sides.index(self.current) + 1})"


c1 = Quaternion(0, 1, 0, 0)
c2 = Quaternion(0, 0, 1, 0)
c3 = Quaternion(0, 0, 0, 1)
c4 = Quaternion(0, 0, 0, -1)
c5 = Quaternion(0, 0, -1, 0)
c6 = Quaternion(0, -1, 0, 0)

cube = {
    c1: {
        "d": c2,
        "r": c3,
        "u": c5,
        "l": c4,
    },
    c2: {
        "d": c3,
        "r": c1,
        "u": c4,
        "l": c6,
    },
    c3: {
        "d": c1,
        "r": c2,
        "u": c6,
        "l": c5,
    },
    c4: {
        "d": c5,
        "r": c6,
        "u": c2,
        "l": c1,
    },
    c5: {
        "d": c6,
        "r": c4,
        "u": c1,
        "l": c3,
    },
    c6: {
        "d": c4,
        "r": c5,
        "u": c3,
        "l": c2,
    },
}

for side, orientation in cube.items():
    print(side, side == orientation["d"] * orientation["r"])

# (prev * curr) * curr  ... forward
# (prev * curr)         ... right
# (curr * prev)         ... left
# curr * (prev * curr)  ... backward


def coord(x: int, size: int = 4) -> int:
    factor = 1 if size % 2 != 0 else 2
    return factor


print(coord(1, size=4))
