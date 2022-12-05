from __future__ import annotations

import argparse
from collections import defaultdict
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    def create_indexed_stacks(line: str) -> dict[int, int]:
        """returns an index of stacks by position of expected item in input"""
        num_items = (len(line) + 1) // 4
        map_index_stacks = {}
        tmp = [1]
        for _ in range(1, num_items):
            tmp.append(tmp[-1] + 4)
        for i, k in enumerate(tmp):
            map_index_stacks[k] = i + 1
        return map_index_stacks

    lines = s.splitlines()
    map_stacks = defaultdict(list)
    indexed_position = create_indexed_stacks(lines[0])
    for line in lines:
        if not line:
            continue
        elif line.startswith("move"):
            # move items as expected
            num_of_items, origin, dest = (int(s) for s in line.split() if s.isdigit())
            for _ in range(num_of_items):
                map_stacks[dest].append(map_stacks[origin].pop())
        else:
            # prepare input stacks
            for char_pos, stack_index in indexed_position.items():
                if line[char_pos].isnumeric():
                    for stack in map_stacks.values():
                        stack.reverse()
                if line[char_pos].isalpha():
                    map_stacks[stack_index].append(line[char_pos])
    return "".join(map_stacks[index][-1] for index in indexed_position.values())


INPUT_S = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
            
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
EXPECTED = "CMZ"


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
