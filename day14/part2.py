from __future__ import annotations

import argparse
from collections import defaultdict
import os.path

import pytest

import support
import itertools


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class CountDone(Exception):
    pass

Blocks = dict[int, set[tuple[int, bool]]]


def pairwise(iterable):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def compute(s: str) -> int:
    blocks = defaultdict(set)
    max_level = float("-inf")

    def move_sand(x: int, y: int, blocks: Blocks) -> int:
        if y > max_level: # 
            raise ValueError("Floor not large enough")
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
                    if y == 0:
                        raise CountDone("Blocked source")
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
            if p1[0] == p2[0]:
                y1, y2 = p1[1], p2[1]
                if y1 < y2:
                    while y1 <= y2:
                        blocks[p1[0]].add(y1)
                        y1 += 1
                else:
                    while y1 >= y2:
                        blocks[p1[0]].add(y2)
                        y2 += 1
            else:
                x1, x2 = p1[0], p2[0]
                if x1 < x2:
                    while x1 <= x2:
                        blocks[x1].add(p1[1])
                        x1 += 1
                else:
                    while x1 >= x2:
                        blocks[x2].add(p1[1])
                        x2 += 1
    # create floor
    max_level += 2
    for x in range(-10000, 10000):
        blocks[x].add(max_level)

    score = 0
    start_x, start_y = (500, 0)
    # let start sand drop
    while True:
        try:
            move_sand(start_x, start_y, blocks)
            score += 1
        except ValueError:
            break
        except CountDone:
            score += 1
            break
    return score


INPUT_S = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
EXPECTED = 93


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
