from __future__ import annotations

import argparse
import os.path
import string

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    def compute_score(c: str) -> int:
        return ord(c) - 96 if c.islower() else ord(c) - 38

    lines = s.splitlines()
    score = 0
    store = {c: 0 for c in list(string.ascii_lowercase) + list(string.ascii_uppercase)}
    tmp_count = 0
    
    for line in lines:
        for c in set(line):
            store[c] += 1
        tmp_count += 1
        if tmp_count == 3:
            for c, count in store.items():
                if count > 2:
                    score += compute_score(c)
                    tmp_count = 0
                    for key in store.keys():
                        store[key] = 0
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
EXPECTED = 70


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
