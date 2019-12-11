from math import atan2, hypot, pi


def angle(a, b):
    # note the y-argument is negated
    return atan2(b[0] - a[0], a[1] - b[1]) % (2 * pi)


def visible(asteroids, a):
    # number visible is equivalent to the number of unique angles
    return len(set(angle(a, b) for b in asteroids if a != b))


def part1(asteroids):
    return max(visible(asteroids, a) for a in asteroids)


def part2(asteroids):
    # station is located at a
    a = max(asteroids, key=lambda a: visible(asteroids, a))
    # no self-destruct :)
    asteroids.remove(a)
    # ranks[b] is how many asteroids {c} are between b and a, i.e.
    # 1) angle(a, c) == angle(a, b)
    # 2) hypot(a, c) < hypot(a, b)
    asteroids.sort(key=lambda b: hypot(b[0] - a[0], b[1] - a[1]))
    ranks = {
        b: sum(angle(a, b) == angle(a, c) for c in asteroids[:i])
        for i, b in enumerate(asteroids)
    }
    # sort by rank, angle
    targets = sorted(asteroids, key=lambda b: (ranks[b], angle(a, b)))
    # return the 200th target
    x, y = targets[199]
    return x * 100 + y


lines = open("input.txt").readlines()

asteroids = [
    (x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char == "#"
]

print(part1(asteroids))
print(part2(asteroids))
