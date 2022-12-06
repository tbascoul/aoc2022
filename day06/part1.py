from __future__ import annotations

import argparse
from collections import deque
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    queue = deque([])
    for i, c in enumerate(s):
        if c in queue:
            while queue:
                poped = queue.popleft()
                if poped == c:
                    queue.append(c)
                    break
        else:
            queue.append(c)
            if len(queue) == 4:
                return i + 1


INPUT_S = """\
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
"""
EXPECTED = 10


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
