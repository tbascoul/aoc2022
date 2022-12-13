from __future__ import annotations

import argparse
from itertools import zip_longest
import os.path

import pytest

import support
from typing import Iterable, Tuple, TypeVar


class InvalidPair(Exception):
    pass


class NextCheck(Exception):
    pass


class ValidPair(Exception):
    pass


T = TypeVar("T")


def grouped(iterable: Iterable[T], n=2) -> Iterable[Tuple[T, ...]]:
    return zip(*[iter(iterable)] * n)


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

is_list = lambda x: isinstance(x, list)
is_int = lambda x: isinstance(x, int)


def validate_pair(l: int | list[int], r: int | list[int]):
    if l is None:
        raise ValidPair()
    if r is None:
        raise InvalidPair("r is None")
    if is_int(l) and is_int(r):
        if l > r:
            raise InvalidPair("l > r")
        elif l == r:
            raise NextCheck()
        else:
            raise ValidPair()
    if is_list(l) and is_int(r):
        r = [r]
    if is_int(l) and is_list(r):
        l = [l]
    if is_list(l) and is_list(r):
        for nl, nr in zip_longest(l, r):
            try:
                validate_pair(nl, nr)
            except NextCheck:
                continue


def compute(s: str) -> int:
    inputs = [eval(line) for line in ["[[2]]", "[[6]]"] + s.splitlines() if line]
    score = 0
    pair_index = 1
    for left, right in grouped(inputs, 2):
        for l, r in zip_longest(left, right):
            try:
                validate_pair(l, r)
            except NextCheck:
                continue
            except InvalidPair:
                break
            except ValidPair:
                score += pair_index
                break
        pair_index += 1
    return score


INPUT_S = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
EXPECTED = 13


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
