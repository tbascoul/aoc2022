from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import os.path

import pytest

import support


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Position:
    x: int
    y: int


def parse_move(line: str) -> tuple[str, int]:
    split = line.split(" ")
    return split[0], int(split[1])


def move_head(move: str, pos: Position):
    match move:
        case "U":
            pos.y += 1
        case "D":
            pos.y -= 1
        case "R":
            pos.x += 1
        case "L":
            pos.x -= 1


def is_touching(head: Position, tail: Position) -> bool:
    if head.x == tail.x and head.y == tail.y:
        return True
    is_one_move_on_y = abs(head.y - tail.y) == 1
    if head.x == tail.x:
        return is_one_move_on_y
    is_one_move_on_x = abs(head.x - tail.x) == 1
    if head.y == tail.y:
        return is_one_move_on_x
    return is_one_move_on_y and is_one_move_on_x  # diagonal pos


def move_tail(head: Position, tail: Position):
    if head.x == tail.x:  # y axis move
        if tail.y < head.y:
            tail.y += 1
        else:
            tail.y -= 1
    elif head.y == tail.y:  # x axis move
        if tail.x < head.x:
            tail.x += 1
        else:
            tail.x -= 1
    else:  # diagonal move
        if tail.x < head.x:
            tail.x += 1
        else:
            tail.x -= 1
        if tail.y < head.y:
            tail.y += 1
        else:
            tail.y -= 1


def compute(s: str) -> int:
    score = defaultdict(set)
    head, tail = Position(0, 0), Position(0, 0)
    for line in s.splitlines():
        move, n = parse_move(line)
        for _ in range(1, n + 1):
            move_head(move, head)
            if not is_touching(head, tail):
                move_tail(head, tail)
            score[tail.x].add(tail.y)
    return sum(sum(1 for _ in values) for values in score.values())


INPUT_S = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
EXPECTED = 13


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


@pytest.mark.parametrize(
    ("head", "tail", "expected"),
    (
        (Position(0, 0), Position(0, 0), True),
        (Position(0, 0), Position(1, 0), True),
        (Position(0, 0), Position(2, 0), False),
        (Position(0, 0), Position(0, 1), True),
        (Position(0, 0), Position(0, 2), False),
        (Position(0, 0), Position(1, 1), True),
        (Position(0, 0), Position(-1, -1), True),
    ),
)
def test_is_touching(head: Position, tail: Position, expected: int) -> None:
    assert is_touching(head, tail) == expected


@pytest.mark.parametrize(
    ("head", "tail", "expected"),
    (
        (Position(2, 0), Position(0, 0), Position(1, 0)),
        (Position(0, 2), Position(0, 0), Position(0, 1)),
        (Position(1, 2), Position(0, 0), Position(1, 1)),
        (Position(2, 1), Position(0, 0), Position(1, 1)),
        (Position(-2, 1), Position(0, 0), Position(-1, 1)),
    ),
)
def test_move_tail(head: Position, tail: Position, expected: Position) -> None:
    move_tail(head, tail)
    assert tail == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
