import sys
import os

sys.path.append("../")
from shared import intcode

SCAFFOLD = 35
ROBOT_UP = 94
ROBOT_RIGHT = 62
ROBOT_LEFT = 60
ROBOT_DOWN = 118
SPACE = 46
NEWLINE = 10


def get_image(outputs):
    x, y = 0, 0
    image = dict()
    for v in outputs:
        image[(x, y)] = v
        x += 1
        if v == NEWLINE:
            y += 1
            x = 0
    return image


def print_image(image):
    x, y = zip(*image.keys())
    xmax, ymax = max(x), max(y)
    for row in range(ymax):
        for col in range(xmax):
            x = col
            y = row
            print(chr(image[(x, y)]), end="")
        print("")


def get_intersections(image):
    intersections = set()
    for (x, y) in image:
        neighbors = [(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        if all(value == SCAFFOLD for value in [image.get(n, 0) for n in neighbors]):
            intersections.add((x, y))
    return intersections


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")

# part 1

vm = intcode.VM()
vm.load_file(filename)
outputs = vm.run([])
image = get_image(outputs)
print_image(image)
intersections = get_intersections(image)
print(sum(x * y for x, y in intersections))

# part 2

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def navigate(image, start, direction=NORTH):
    x, y = start
    instructions = []
    dxdy = {NORTH: (0, -1), EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0)}
    while True:
        dx, dy = dxdy[direction]
        ahead = (x + dx, y + dy)
        if image.get(ahead, SPACE) == SCAFFOLD:
            if isinstance(instructions[-1], int):
                instructions[-1] += 1
            else:
                instructions.append(1)
            x += dx
            y += dy
            continue
        if image.get(ahead, SPACE) in [SPACE, NEWLINE]:
            # check left turn
            dx, dy = dxdy[(direction - 1) % 4]
            if image.get((x + dx, y + dy), SPACE) == SCAFFOLD:
                instructions.append("L")
                direction = (direction - 1) % 4
                continue
            # check right turn
            dx, dy = dxdy[(direction + 1) % 4]
            if image.get((x + dx, y + dy), SPACE) == SCAFFOLD:
                instructions.append("R")
                direction = (direction + 1) % 4
                continue
        break
    return list(map(str, instructions))


vm = intcode.VM()
vm.load_file(filename)
vm.write(0, 2, mode=1)  # wake the robot

ch2dir = {ROBOT_UP: 0, ROBOT_RIGHT: 1, ROBOT_DOWN: 2, ROBOT_LEFT: 3}

startpos = None
startdir = None
for (x, y), v in image.items():
    if v in ch2dir:
        startpos = (x, y)
        startdir = ch2dir[v]
        break

print(startpos, startdir)
instructions = navigate(image, startpos, startdir)
print(instructions)


def find_subroutines(instructions):
    # we know that the first substring must start from the first instruction
    # and that the last substring must end with the last instruction
    # so we can brute force all possible A and C and see if the remaining fragments are covered by the shortest fragment
    n = len(instructions)
    # brute force all possible A and C (100 possibilities total)
    for a in range(1, 10):
        A = instructions[0:a]
        for c in range(1, 10):
            C = instructions[-c:]
            covered = [False for i in instructions]
            # update coverage due to A
            for i in range(n - len(A)):
                if instructions[i : (i + len(A))] == A:
                    for j in range(i, i + len(A)):
                        covered[j] = True
            # update coverage due to B
            for i in range(n - len(C)):
                if instructions[i : (i + len(C))] == C:
                    for j in range(i, i + len(C)):
                        covered[j] = True
            # get fragments not covered by A or C, and keep track of shortest fragment
            fragments = []
            fragment = []
            shortest = [0] * n
            for i in range(n):
                if covered[i] is True:
                    if len(fragment) > 0:
                        fragments.append(fragment.copy())
                        if len(fragment) < len(shortest):
                            shortest = fragment.copy()
                    else:
                        continue
                if covered[i] is False:
                    fragment.append(instructions[i])
            # check if the shortest fragment covers longer fragments
            valid = True
            for fragment in fragments:
                if shortest == fragment:
                    continue
                elif len(shortest) < len(fragment):
                    reps = len(fragment) // len(shortest)
                    if shortest * reps == fragment:
                        continue
                valid = False
                break
            # print out comprresion
            if valid:
                B = shortest
                Istr = ",".join(instructions)
                Astr = ",".join(A)
                Bstr = ",".join(B)
                Cstr = ",".join(C)
                compressed = (
                    Istr.replace(Astr, "A").replace(Bstr, "B").replace(Cstr, "C")
                )
                print(compressed, Astr, Bstr, Cstr, sep="\n")
                return compressed, Astr, Bstr, Cstr

    pass


I, A, B, C = find_subroutines(instructions)

main_routine = [ord(c) for c in f"{I}\n"]
fa = [ord(c) for c in f"{A}\n"]
fb = [ord(c) for c in f"{B}\n"]
fc = [ord(c) for c in f"{C}\n"]
viz = [ord(c) for c in "n\n"]  # no viz

outputs = vm.run(main_routine + fa + fb + fc + viz)
print(outputs[-1])
