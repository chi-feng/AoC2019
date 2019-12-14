import sys
import numpy as np
import time
import curses
import os

sys.path.append("../")
from shared import intcode


def part1():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "input.txt")
    vm = intcode.VM()
    vm.load_file(filename)
    screen = dict()
    while True:
        status = vm.step()
        if len(vm.outputs) == 3:
            x, y, t = vm.outputs
            screen[(x, y)] = t
            vm.outputs = []
        if status == vm.HALT:
            break
    return sum(v == 2 for k, v in screen.items())


def part2():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "input.txt")
    vm = intcode.VM()
    vm.load_file(filename)
    vm.write(0, 2, 1)  # put 2 quarters into machine
    screen = dict()
    score = 0
    while True:
        status = vm.step()
        if len(vm.outputs) == 3:
            x, y, t = vm.outputs
            screen[(x, y)] = t
            vm.outputs = []
            if x == -1:
                score = t
            if t == 3:
                paddle_x = x
            if t == 4:
                ball_x = x
        if status == vm.WAIT:
            vm.inputs.append(np.sign(ball_x - paddle_x))
        if status == vm.HALT:
            break
    return score


def animate(stdscr):
    ROWS = 22 + 2
    COLS = 44 + 2
    win = curses.newwin(ROWS, COLS)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    vm = intcode.VM()
    vm.load_file("input.txt")
    vm.write(0, 2, 1)  # put quarter into machine
    screen = dict()
    score = 0
    charcode = {0: " ", 1: "█", 2: "▢", 3: "▁", 4: "●"}
    while True:
        status = vm.step()
        if len(vm.outputs) == 3:
            x, y, t = vm.outputs
            screen[(x, y)] = t
            vm.outputs = []
            if x == -1:
                score = t
            if t == 3:
                paddle_x = x
            if t == 4:
                ball_x = x
        if status == vm.WAIT:
            vm.inputs.append(np.sign(ball_x - paddle_x))
            win.clear()
            for (x, y) in screen:
                if x < 0:
                    continue
                win.addch(y + 1, x, charcode[screen[x, y]])
            win.addstr(0, 0, f"SCORE: {score}")
            win.refresh()
            time.sleep(0.015)
        if status == vm.HALT:
            break
    # Clean up before exiting
    curses.nocbreak()
    win.keypad(0)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    print(part1())
    print(part2())
    print("Press ENTER to continue")
    input()
    curses.wrapper(animate)
