from math import gcd
from functools import reduce
import numpy as np


class Moon:
    def __init__(self, x, y, z):
        self.pos = np.array([int(x), int(y), int(z)], dtype=int)
        self.vel = np.array([0, 0, 0], dtype=int)


def read_input(filename):
    """Read input file where each line is in the format `<x=-1, y=0, z=2>`"""
    moons = []
    with open(filename, "r") as file:
        for line in file.readlines():
            tokens = line.strip()[1:-1].split(", ")
            x, y, z = int(tokens[0][2:]), int(tokens[1][2:]), int(tokens[2][2:])
            moon = Moon(x, y, z)
            moons.append(moon)
    return moons


def step(moons):
    for i, a in enumerate(moons):
        for j, b in enumerate(moons):
            if j >= i:
                continue
            # apply gravity
            d = np.sign(b.pos - a.pos)
            a.vel += d
            b.vel -= d
    for i, a in enumerate(moons):
        # add velocity to position
        a.pos += a.vel


def part1(filename, steps=1):
    moons = read_input(filename)
    for k in range(steps):
        step(moons)
    etot = 0
    for i, a in enumerate(moons):
        epot = np.sum(np.abs(a.pos))
        ekin = np.sum(np.abs(a.vel))
        etot += epot * ekin
    return etot


def lcm(numbers):
    return reduce(lambda a, b: a * b // gcd(a, b), numbers)


def part2(filename):
    moons = read_input(filename)
    initial = [
        tuple(a.pos[i] for a in moons) + tuple(a.vel[i] for a in moons)
        for i in range(3)
    ]
    periods = [0, 0, 0]
    k = 0
    while True:
        k += 1
        step(moons)
        # check for a full period in each dimension (independently)
        for i in range(3):
            state = tuple(a.pos[i] for a in moons) + tuple(a.vel[i] for a in moons)
            if periods[i] == 0 and state == initial[i]:
                periods[i] = k
        # stop if all periods have been found
        if all(periods):
            break
    print(periods)
    return lcm(periods)


if __name__ == "__main__":
    assert part1("test1.txt", 10) == 179
    assert part1("test2.txt", 100) == 1940
    print(part1("input.txt", 1000))  # 8044

    assert part2("test1.txt") == 2772
    print(part2("input.txt"))  # 362375881472136
