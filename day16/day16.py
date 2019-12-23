import sys
import os
import numpy as np
import time


def part1(input_str, phases):
    base_pattern = np.array([0, 1, 0, -1], dtype=int)
    input_list = np.array(list(map(int, input_str)), dtype=int)
    n = len(input_list)
    patterns = dict()
    for position in range(1, n + 1):
        reps = n // (position * len(base_pattern)) + 1
        patterns[position] = np.tile(base_pattern.repeat(position), reps)[1 : n + 1]
    for _ in range(phases):
        out = np.zeros(n, dtype=int)
        for position in range(1, n + 1):
            out[position - 1] = np.dot(input_list, patterns[position])
        input_list = np.abs(out) % 10
    result = "".join(map(str, input_list))
    print(f"After {phases} phases: {result}")
    print("First 8 digits", result[:8])


def part2(input_str, phases=4):

    offset = int(input_str[:7])
    input_list = np.tile(np.array(list(map(int, input_str))), 10000)
    input_length = len(input_list)

    for i in range(phases):
        print(i)
        partial_sum = np.sum(input_list[offset:])
        for j in range(offset, input_length):
            t = partial_sum
            partial_sum -= input_list[j]
            input_list[j] = abs(t) % 10

    print(input_list[offset : offset + 8])


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "input.txt")
    input_str = open(filename).readline().strip()

    start_time = time.time()
    part1(input_str, 100)
    end_time = time.time()
    print("part 1", end_time - start_time)

    part2("12345678")
