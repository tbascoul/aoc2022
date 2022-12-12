from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
import os.path

import pytest

import support


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Position:
    v: int
    is_visited: bool

def compute(s: str) -> int:
    m: list[list[Position]] = []
    start = None
    for y, line in enumerate(s.splitlines()):
        tmp = []
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y, 0, 0)
                tmp.append(Position(-1, False))
            elif c == "E":
                tmp.append(Position(42, False))
            else:
                tmp.append(Position(ord(c), False))
        m.append(tmp)
    len_x, len_y = len(m[0]) - 1, len(m) - 1
    min_score = float("inf")
    queue = deque([start])
    while queue:
        x, y, prev_val, score = queue.popleft()
        if x < 0 or x > len_x or y < 0 or y > len_y or m[y][x].is_visited:
            continue
        if m[y][x].v == 42 and chr(prev_val) == "z": # end cell
            min_score = min(min_score, score)
            continue
        if prev_val == -1 or m[y][x].v == -1 or 0 <= m[y][x].v - prev_val <= 1:
            score += 1
            queue.append((x + 1, y, m[y][x].v, score))
            queue.append((x - 1, y, m[y][x].v, score))
            queue.append((x, y + 1, m[y][x].v, score))
            queue.append((x, y - 1, m[y][x].v, score))
            m[y][x].is_visited = True

    return min_score


INPUT_S = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
EXPECTED = 31


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
