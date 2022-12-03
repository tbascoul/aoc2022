from __future__ import annotations

import argparse
import os.path
from typing import Counter

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()
    score = 0
    for line in lines:
        mid = len(line) / 2
        if not mid.is_integer():
            raise ValueError("Unexpected len for input")
        mid = int(mid)
        w1, w2 = line[:mid], line[mid:]
        unique_w2 = set(w2)
        for c in w1:
            if c in unique_w2:
                if not c.isalpha():
                    raise ValueError("Accept only letters")
                char_score = ord(c) - 96 if c.islower() else ord(c) - 38
                score += char_score
                break
    return score


INPUT_S = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
EXPECTED = 157


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
