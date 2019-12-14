from .day12 import part1, part2


def test_part1():
    assert part1("test1.txt", 10) == 179
    assert part1("test2.txt", 100) == 1940


def test_day2():
    assert part2("test1.txt") == 2772
