from .day14 import part1, part2

def test_part1():
    assert part1("test1.txt") == 13312
    assert part1("test2.txt") == 180697


def test_part2():
    assert part2("test1.txt") == 82892753
    assert part2("test2.txt") == 5586022
