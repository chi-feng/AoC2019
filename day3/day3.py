dxdy = {'U': (0, 1), 'R': (1, 0), 'D': (0, -1), 'L': (-1, 0)}

def get_coords(path):
    # coords[(x, y)] = minimum number of steps to reach (x, y)
    coords = dict()
    x, y = 0, 0
    steps = 0
    for segment in path:
        dx, dy = dxdy[segment[0]]
        length = int(segment[1:])
        for i in range(length):
            x += dx
            y += dy
            steps += 1
            if (x, y) not in coords: 
                coords[(x, y)] = steps
    return coords

with open("input.txt") as file:
    A = get_coords(file.readline().split(","))
    B = get_coords(file.readline().split(","))

intersections = set(A.keys()) & set(B.keys())

print('min distance', min(abs(x) + abs(y) for x, y in intersections))
print('min path length', min(A[c] + B[c] for c in intersections))
