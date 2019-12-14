from day12 import day12


def test_part1():
    assert day12.part1("test1.txt", 10) == 179
    assert day12.part1("test2.txt", 100) == 1940


def test_day2():
    assert day12.part2("test1.txt") == 2772
