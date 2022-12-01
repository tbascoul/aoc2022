from __future__ import annotations

import argparse
import heapq
import os.path

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, top_n: int) -> int:
    current_sum = 0
    max_heap = []
    for line in s.splitlines(): 
        try:
            current_sum += int(line)
        except ValueError:
            heapq.heappush(max_heap, current_sum * (-1))
            current_sum = 0
    return sum([heapq.heappop(max_heap) for _ in range(top_n)]) * (-1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 3))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
