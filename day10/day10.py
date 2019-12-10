import numpy as np

asteroids = []

with open("input2.txt") as file:
    lines = file.readlines()
    xmax = len(lines[0].strip()) - 1
    ymax = len(lines) - 1
    for i, line in enumerate(lines):
        for j, c in enumerate(line.strip()):
            if c == '#':
                asteroids.append((j,i))

def get_visible(asteroids, a):
    visible = {c: True for c in asteroids}
    visible[a] = False # can't see itself 
    for b in asteroids:
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        if dx == 0 and dy == 0:
            continue
        if dx == 0:
            dy = np.sign(dy)
        elif dy == 0:
            dx = np.sign(dx)
        else:
            gcd = np.gcd(dx, dy)
            dx = dx // gcd
            dy = dy // gcd
        # go in the direction of (dx,dy) starting from b, and mark as not visible
        k = 1
        x, y = b[0] + k * dx, b[1] + k * dy
        while 0 <= x <= xmax and 0 <= y <= ymax:
            if (x, y) in visible:
                visible[(x, y)] = False
            k += 1
            x, y = b[0] + k * dx, b[1] + k * dy
    return {c for c in asteroids if visible[c]}

visible_count = [len(get_visible(asteroids, a)) for a in asteroids]

max_count = max(visible_count)
station = asteroids[visible_count.index(max_count)]
print(station, 'visible', max_count) # (29, 28), 256

# laser time

def get_angle(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    v = np.pi / 2 - np.arctan2(-dy, dx)
    if v < 0:
        v += 2 * np.pi
    return v

visible = get_visible(asteroids, station)
angle = 0
vaporized = []
while len(visible) > 0:
    angles = {a: get_angle(a, station) for a in visible if get_angle(a, station) >= angle}
    targets = sorted(angles, key=angles.get)
    vaporized.append(targets[0])
    asteroids.remove(targets[0])
    if len(targets) == 1:
        angle = 0
    else:
        angle = get_angle(targets[1], station)
    visible = get_visible(asteroids, station)

for i, target in enumerate(vaporized):
    print(i+1, target)