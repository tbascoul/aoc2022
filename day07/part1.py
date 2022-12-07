from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

from dataclasses import dataclass, field

# Find all of the directories with a total size of at most 100000.
# What is the sum of the total sizes of those directories?


@dataclass
class Node:
    prev: Node | None
    children: dict[str, Node] = field(default_factory=dict)
    size: int = 0


def compute(s: str) -> int:
    sum_sub_100k_dir = 0
    current_n = Node(prev=None)
    for line in s.splitlines():
        if line in ["$ cd /", "$ ls"]:
            continue
        elif line.startswith("dir"):
            # create new dir as a children of current dir
            dir_name = line.split(" ")[-1]
            current_n.children[dir_name] = Node(prev=current_n)
        elif line.startswith("$ cd"):
            dir_name = line.split(" ")[-1]
            if dir_name == "..":
                # move to prev node with computed size
                folder_size = current_n.size
                if folder_size < 100_000:
                    sum_sub_100k_dir += folder_size
                current_n = current_n.prev
                current_n.size += folder_size
            else:
                # move to children node
                current_n = current_n.children[dir_name]
        else:
            # expect file size input
            if not line:
                raise ValueError("Unexpected input")
            file_size = int(line.split(" ")[0])
            current_n.size += file_size

    # move back to parent dir
    while current_n.prev:
        folder_size = current_n.size
        if folder_size < 100_000:
            sum_sub_100k_dir += folder_size
        current_n = current_n.prev
        current_n.size += folder_size

    return sum_sub_100k_dir


INPUT_S = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
EXPECTED = 95437


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
