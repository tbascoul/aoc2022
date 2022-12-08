from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def validate_tree(
    m: list[list[int]], x: int, y: int, len_x: int, len_y: int, current: int, move: str
) -> bool:
    match move:
        case "left":
            if x < 0 or m[x][y] >= current:
                return False
            if x == 0:
                return m[x][y] < current
            return validate_tree(m, x - 1, y, len_x, len_y, current, "left")
        case "right":
            if x > len_x - 1 or m[x][y] >= current:
                return False
            if x == len_x - 1:
                return m[x][y] < current
            return validate_tree(m, x + 1, y, len_x, len_y, current, "right")
        case "up":
            if y < 0 or m[x][y] >= current:
                return False
            if y == 0:
                return m[x][y] < current
            return validate_tree(m, x, y - 1, len_x, len_y, current, "up")
        case "down":
            if y > len_y - 1 or m[x][y] >= current:
                return False
            if y == len_y - 1:
                return m[x][y] < current
            return validate_tree(m, x, y + 1, len_x, len_y, current, "down")
        case _:
            raise ValueError("Unexpected move")


def compute(s: str) -> int:
    m = []
    for line in s.splitlines():
        m.append([int(c) for c in line])
    len_x, len_y = len(m[0]), len(m)
    score = (len_x + len_y) * 2 - 4
    for x in range(1, len_x - 1):
        for y in range(1, len_y - 1):
            is_valid = (
                validate_tree(m, x - 1, y, len_x, len_y, m[x][y], "left")
                or validate_tree(m, x + 1, y, len_x, len_y, m[x][y], "right")
                or validate_tree(m, x, y - 1, len_x, len_y, m[x][y], "up")
                or validate_tree(m, x, y + 1, len_x, len_y, m[x][y], "down")
            )
            score += is_valid
    return score


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 21


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
