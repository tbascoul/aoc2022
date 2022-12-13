from __future__ import annotations

import argparse
from collections import deque
import os.path

import pytest

import support


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    m = s.splitlines()
    queue = deque(
        (i, j, 0, "a")
        for i in range(len(m))
        for j in range(len(m[i]))
        if m[i][j] == "S"
    )
    min_score = float("inf")
    visited = set((i, j) for i, j, _, _ in queue)
    while queue:
        i, j, score, prev = queue.popleft()
        if m[i][j] == "E":
            min_score = min(score, min_score)
            continue
        for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):
            if not (0 <= x < len(m)) or not (0 <= y < len(m[x])) or (x, y) in visited:
                continue
            curr = m[x][y].replace("E", "z")
            if ord(curr) > ord(prev) + 1:
                continue
            visited.add((x, y))
            queue.append((x, y, score + 1, curr))
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
