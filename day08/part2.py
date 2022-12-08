from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def can_see_x_trees(
    m: list[list[int]],
    x: int,
    y: int,
    len_x: int,
    len_y: int,
    current: int,
    move: str,
    score: int = 1,
) -> int:
    match move:
        case "left":
            if x == 0 or m[y][x] >= current:
                return score
            return can_see_x_trees(
                m, x - 1, y, len_x, len_y, current, "left", score + 1
            )
        case "right":
            if x == len_x - 1 or m[y][x] >= current:
                return score
            return can_see_x_trees(
                m, x + 1, y, len_x, len_y, current, "right", score + 1
            )
        case "up":
            if y == 0 or m[y][x] >= current:
                return score
            return can_see_x_trees(m, x, y - 1, len_x, len_y, current, "up", score + 1)
        case "down":
            if y == len_y - 1 or m[y][x] >= current:
                return score
            return can_see_x_trees(
                m, x, y + 1, len_x, len_y, current, "down", score + 1
            )
        case _:
            raise ValueError("Unexpected move")


def compute(s: str) -> int:
    m = []
    for line in s.splitlines():
        m.append([int(c) for c in line])
    len_x, len_y = len(m[0]), len(m)
    score = float("-inf")
    for y in range(1, len_y - 1):
        for x in range(1, len_x - 1):
            tmp_score = (
                can_see_x_trees(m, x - 1, y, len_x, len_y, m[y][x], "left")
                * can_see_x_trees(m, x + 1, y, len_x, len_y, m[y][x], "right")
                * can_see_x_trees(m, x, y - 1, len_x, len_y, m[y][x], "up")
                * can_see_x_trees(m, x, y + 1, len_x, len_y, m[y][x], "down")
            )
            score = max(score, tmp_score)
    return score


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 8


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
