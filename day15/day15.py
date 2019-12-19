import sys
import os
from collections import defaultdict
import curses
import time


sys.path.append("../")
from shared import intcode

UNEXPLORED = 0
PATH = 1
WALL = 2
TARGET = 3

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


def draw_maze(maze, path=[], node=None, direction=None):
    x, y = zip(*maze.keys())
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    maze_string = []
    for row in range(ymax - ymin + 1):
        for col in range(xmax - xmin + 1):
            x = col + xmin
            y = ymax - row
            cell = maze[(x, y)]
            ch = "░"
            if cell == PATH:
                ch = " "
            if cell == WALL:
                ch = "█"
            if (x, y) in path:
                ch = "·"
            if cell == TARGET:
                ch = "B"
            if (x, y) == (0, 0):
                ch = "A"
            if node and (x, y) == node:
                chdir = {NORTH: "▲", EAST: "►", SOUTH: "▼", WEST: "◄"}
                ch = chdir[direction]
            # print(ch, end="")
            maze_string.append(ch)
        maze_string.append("\n")
    print("".join(maze_string))


def adjacent(node):
    x, y = node
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def is_dead_end(maze, node):
    return sum(maze[node] == WALL for node in adjacent(node)) >= 3


def explore(node, maze, vm):  # DFS, explore adjacent nodes and backtrack at dead ends
    if is_dead_end(maze, node):
        return
    dxdy = {NORTH: (0, 1), SOUTH: (0, -1), WEST: (-1, 0), EAST: (1, 0)}  # NSWE
    opposite = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}  # for backtracking
    for direction in [NORTH, SOUTH, WEST, EAST]:
        dx, dy = dxdy[direction]
        new = (node[0] + dx, node[1] + dy)
        if maze[new] in {PATH, TARGET}:
            draw_maze(maze, node=new, direction=direction)
            time.sleep(0.032)
        if maze[new] == UNEXPLORED:
            # issue move command to robot and read status (first output)
            status = vm.run(inputs=[direction])[0]
            if status == 0:  # hit wall
                maze[new] = WALL
            elif status > 0:  # move successful
                maze[new] = TARGET if status == 2 else PATH
                draw_maze(maze, node=new, direction=direction)
                time.sleep(0.032)
                explore(new, maze, vm)
                # backtrack by issuing move command in opposite direction
                vm.run(inputs=[opposite[direction]])[0]


def shortest_path_bfs(maze, start, goal):
    visited = set()
    queue = [[start]]
    while len(queue) > 0:
        path = queue.pop(0)
        node = path[-1]
        if node not in visited:
            for neighbor in [n for n in adjacent(node) if maze[node] in {PATH, TARGET}]:
                new_path = path.copy()
                new_path.append(neighbor)
                queue.append(new_path)
                if neighbor == goal:
                    return new_path
            visited.add(node)


def get_distances(maze, start):
    visited = set()
    queue = [[start]]
    distances = defaultdict(lambda: -1)
    while len(queue) > 0:
        path = queue.pop(0)
        node = path[-1]
        if node not in visited:
            for neighbor in [n for n in adjacent(node) if maze[node] in {PATH, TARGET}]:
                new_path = path.copy()
                new_path.append(neighbor)
                queue.append(new_path)
            visited.add(node)
            distances[node] = len(path) - 2
    return distances


def plot_distances(maze, distances):
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    x, y = zip(*maze.keys())
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    rows = ymax - ymin + 1
    cols = xmax - xmin + 1
    import numpy as np

    Z = np.zeros((rows, cols))
    target = None
    for row in range(rows):
        for col in range(cols):
            x = col + xmin
            y = ymax - row
            cell = maze[(x, y)]
            distance = distances[(x, y)]
            Z[row, col] = distance
            if cell == WALL or cell == UNEXPLORED:
                Z[row, col] = np.nan
            if cell == TARGET:
                target = (col, row)
    plt.imshow(Z)
    plt.colorbar()
    plt.plot(target[0], target[1], "ro")
    # plt.show()
    plt.savefig("day15.png")


def part1(filename):

    vm = intcode.VM()
    vm.load_file(filename)

    start = (0, 0)
    maze = defaultdict(lambda: UNEXPLORED)
    maze[start] = PATH
    explore(start, maze, vm)

    target = [n for n in maze if maze[n] == TARGET][0]
    print(f"Found Oxygen System at {target}")

    shortest_path = shortest_path_bfs(maze, start, target)
    print(f"Shortest path {len(shortest_path)}")
    draw_maze(maze, shortest_path)

    distances = get_distances(maze, target)
    print(f"Max distance from OS: {max(distances.values())}")
    plot_distances(maze, distances)


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "input.txt")
    part1(filename)
    """
    Found Oxygen System at (-16, 12)
    Shortest path 241
    Max distance from OS: 322
    """
