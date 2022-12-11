from __future__ import annotations

import argparse
import os.path

import pytest

import support


INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


# addx V takes two cycles to complete. After two cycles,
# the X register is increased by the value V. (V can be negative.)
# noop takes one cycle to complete. It has no other effect.


# During the 20th cycle, register X has the value 21, so the signal strength is 20 * 21 = 420.
# (The 20th cycle occurs in the middle of the second addx -1,
# so the value of register X is the starting value, 1,
# plus all of the other addx values up to that point: 1 + 15 - 11 + 6 - 3 + 5 - 1 - 8 + 13 + 4 = 21.)


def parse_v(line: str) -> int:
    split = line.split(" ")
    return int(split[1])

def get_sprite_pos(x: int) -> set[int]:
    return {x-1,x,x+1}


def compute(s: str) -> int:
    x, cycle = 1, 0
    output = "" # should use matrix :x
    stripe_pos = get_sprite_pos(x)
    lines = s.splitlines()
    for line in lines:
        if line == "noop":
            required_cycles, v = (1, None)
        else:
            required_cycles, v = (2, parse_v(line))
        while required_cycles:
            required_cycles -= 1
            cycle += 1
            if not required_cycles and v:
                x += v
                stripe_pos = get_sprite_pos(x)
            if cycle in stripe_pos:
                output += "#"
            else:
                output += "."
            if cycle == 40:
                output += "\n"
                cycle = 0
    return output


INPUT_S = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""
EXPECTED = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""


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
