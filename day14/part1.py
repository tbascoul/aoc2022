from __future__ import annotations

import argparse
from collections import defaultdict
import os.path

import pytest

import support
import itertools


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

Blocks = dict[int, set[int]]


def pairwise(iterable):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def compute(s: str) -> int:
    blocks = defaultdict(set)
    max_level = float("-inf")

    def move_sand(x: int, y: int, blocks: Blocks) -> int:
        if y > max_level:
            raise ValueError("Infinity glitch")
        has_below_block = y + 1 in blocks.get(x, ())
        if not has_below_block:
            return move_sand(x, y + 1, blocks)
        else:
            has_left_block = y + 1 in blocks.get(x - 1, ())
            if not has_left_block:
                return move_sand(x - 1, y + 1, blocks)
            else:
                has_right_block = y + 1 in blocks.get(x + 1, ())
                if not has_right_block:
                    return move_sand(x + 1, y + 1, blocks)
                else:
                    blocks[x].add(y)
                    return y

    # note all blocks positions
    for line in s.splitlines():
        pairs = []
        for position in line.split(" -> "):
            x, y = position.split(",")
            x, y = int(x), int(y)
            max_level = max(max_level, y)
            pairs.append((x, y))
        for p1, p2 in pairwise(pairs):
            x1, x2, y1, y2 = p1[0], p2[0], p1[1], p2[1]
            if x1 == x2:
                if y1 < y2:
                    while y1 <= y2:
                        blocks[x1].add(y1)
                        y1 += 1
                else:
                    while y1 >= y2:
                        blocks[x1].add(y2)
                        y2 += 1
            else:
                if x1 < x2:
                    while x1 <= x2:
                        blocks[x1].add(y1)
                        x1 += 1
                else:
                    while x1 >= x2:
                        blocks[x2].add(y1)
                        x2 += 1

    score = 0
    # let start sand drop
    while True:
        try:
            move_sand(500, 0, blocks)
        except ValueError:
            break
        score += 1
    return score


INPUT_S = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
EXPECTED = 24


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
