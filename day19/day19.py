import os, sys

sys.path.append("../")
from shared import intcode


def print_screen(screen):
    x, y = zip(*screen.keys())
    xmax, ymax = max(x), max(y)
    ss = []
    ss.append("  ")
    for col in range(xmax):
        ss.append(f"{col:2d}")
    ss.append("\n")
    for row in range(ymax):
        ss.append(f"{row:2d}")
        for col in range(xmax):
            x = col
            y = row
            ss.append(f"{screen[(x, y)]:2d}")
        ss.append("\n")
    print("".join(ss))


def part1():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "input.txt")
    vm = intcode.VM()
    vm.load_file(filename)
    screen = dict()
    for x in range(50):
        for y in range(50):
            outputs = vm.copy().run([x, y])
            screen[(x, y)] = outputs[-1]
    print(sum(c == 1 for (x, y), c in screen.items()))
    print_screen(screen)


def get_value(vm, x, y):
    return vm.copy().run([x, y])[-1]


def part2():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "input.txt")
    vm = intcode.VM()
    vm.load_file(filename)
    x = 100
    y = 100
    # get into the beam
    while get_value(vm, x, y) == 0:
        x += 1
    while True:
        # check if box of size 100x100 fits
        if get_value(vm, x + 99, y - 99) == 1:
            print(10000 * x + (y - 99))
            break
        # move down, then right until we find 1
        y += 1
        while get_value(vm, x, y) == 0:
            x += 1


if __name__ == "__main__":
    part1()
    part2()
