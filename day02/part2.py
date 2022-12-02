from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

# Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock
# A for Rock, B for Paper, and C for Scissors
# X for Rock, Y for Paper, and Z for Scissors

# strat
# A Y
# B X
# C Z

# score
# points for pick: 1 for Rock, 2 for Paper, and 3 for Scissors
# points for outcome: 0 if you lost, 3 if the round was a draw, and 6 if you won

# part2
# X means you need to lose
# Y means you need to end the round in a draw
# and Z means you need to win.


def compute(s: str) -> int:
    def points_for_action(p1: str, action: str) -> int:
        match action:
            case "X":  # must lose
                match p1:
                    case "A":
                        return points_for_pick("Z")
                    case "B":
                        return points_for_pick("X")
                    case "C":
                        return points_for_pick("Y")
            case "Y":  # must draw
                return points_for_pick(translate_col(p1)) + 3
            case "Z":  # must win
                match p1:
                    case "A":
                        return points_for_pick("Y") + 6
                    case "B":
                        return points_for_pick("Z") + 6
                    case "C":
                        return points_for_pick("X") + 6

    def points_for_pick(pick: str) -> int:
        match pick:
            case "X":
                return 1
            case "Y":
                return 2
            case "Z":
                return 3

    def translate_col(pick: str) -> str:
        match pick:
            case "A":
                return "X"
            case "B":
                return "Y"
            case "C":
                return "Z"

    lines = s.splitlines()
    score = 0
    for line in lines:
        p1, action = line.split(" ")
        score += points_for_action(p1, action)
    return score


INPUT_S = """\
A Y
B X
C Z
"""
EXPECTED = 12


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
