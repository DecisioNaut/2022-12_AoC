from functools import reduce

from typing import TypeVar, Callable

T = TypeVar("T")


def chain(*fs: Callable[[T], T]) -> Callable[[T], T]:
    """Chaines functions to a single function."""

    def chained(x: T) -> T:
        return reduce((lambda _x, f: f(_x)), fs, x)

    return chained


def f1(x: int) -> int:
    return x + 1


def f2(x: int) -> int:
    return 2 * x

