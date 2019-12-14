import os
import sys

dirname = os.path.dirname(__file__)

sys.path.append("../")

print(sys.path)
from shared import intcode


class Robot:
    def __init__(self, program):
        self.program = program
        self.computer = intcode.VM()
        self.computer.load(program)
        self.direction = 0
        # north
        self.dxdy = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
        self.x = 0
        self.y = 0

    def send_color(self, c):
        return self.computer.run(inputs=[c])

    def turn_left(self):
        self.direction -= 1
        if self.direction == -1:
            self.direction = 3

    def turn_right(self):
        self.direction += 1
        if self.direction == 4:
            self.direction = 0

    def move(self):
        dx, dy = self.dxdy[self.direction]
        self.x += dx
        self.y += dy


filename = os.path.join(dirname, "input.txt")
program = list(map(int, open(filename).readline().strip().split(",")))

r = Robot(program)

colors = dict()
colors[(0, 0)] = 1

painted_panels = set()

while True:

    color = colors.get((r.x, r.y), 0)

    print(f"({r.x:2d}, {r.y:2d}) direction {r.direction} input {color}", end=" ")
    outputs = r.send_color(color)

    paint_color, direction = outputs[0], outputs[1]
    print(f"output {outputs}", end=" ")
    print("paint", color, "->", paint_color)

    colors[(r.x, r.y)] = paint_color

    if color != paint_color:
        painted_panels.add((r.x, r.y))

    if direction == 0:
        r.turn_left()
    if direction == 1:
        r.turn_right()
    r.move()

    if r.computer.status == 1:
        break

print(len(painted_panels))

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt

white = [k for k, v in colors.items() if v == 1]
x, y = zip(*white)
plt.figure(figsize=(4, 0.6))
plt.plot(x, y, "ko")
plt.savefig("output.png")
