from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int

    def __post_init__(self):
        self.start = int(self.start)
        self.end = int(self.end)


def compute(s: str) -> int:
    lines = s.splitlines()
    score = 0
    for line in lines:
        r1, r2 = (Range(*range.split("-")) for range in line.split(","))
        if (r1.start <= r2.start and r2.end <= r1.end) or (
            r2.start <= r1.start and r1.end <= r2.end
        ):
            score += 1
    return score


INPUT_S = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
EXPECTED = 2


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
