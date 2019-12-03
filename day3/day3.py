dxdy = {'U': (0, 1), 'R': (1, 0), 'D': (0, -1), 'L': (-1, 0)}

# get a dictionary mapping coords to the min number of steps to reach that coord
def get_coord_steps(path):
    coords = dict()
    x, y = 0, 0
    steps = 0
    for segment in path.split(","):
        direction = segment[0]
        dx, dy = dxdy[direction]
        length = int(segment[1:])
        for i in range(length):
            steps += 1
            x += dx
            y += dy
            if (x, y) not in coords: 
                coords[(x, y)] = steps
    return coords


def get_intersections(paths):
    """ Returns a data structure like
        {(3, 3): {'distance': 6, 'steps': (20, 20)}, 
         (6, 5): {'distance': 11, 'steps': (15, 15)}} """
    A_steps = get_coord_steps(paths[0])
    B_steps = get_coord_steps(paths[1])
    intersections = set(A_steps.keys()) & set(B_steps.keys())
    return {coord: {'distance': abs(coord[0]) + abs(coord[1]), 
                    'steps': (A_steps[coord], B_steps[coord])} for coord in intersections}


def get_closest_intersection(intersections):
    coords = intersections.keys()
    coords_sorted = sorted(coords, key=lambda coord: intersections[coord]['distance'])
    return intersections[coords_sorted[0]]


def get_fastest_intersection(intersections):
    coords_sorted = sorted(intersections.keys(), key=lambda c: sum(intersections[c]['steps']))
    return intersections[coords_sorted[0]]


""" TEST CASE
...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
{(3, 3): {'distance': 6, 'steps': (20, 20)}, 
 (6, 5): {'distance': 11, 'steps': (15, 15)}}
Closest intersection {'distance': 6, 'steps': (20, 20)}
Fastest intersection {'distance': 11, 'steps': (15, 15)} 
"""
test_paths = ['R8,U5,L5,D3', 'U7,R6,D4,L4']
intersections = get_intersections(test_paths)
print(intersections)
print('Closest intersection %r' % get_closest_intersection(intersections))
print('Fastest intersection %r' % get_fastest_intersection(intersections))


""" 
Closest intersection {'distance': 4981, 'steps': (30677, 141959)}
Fastest intersection {'distance': 8968, 'steps': (35266, 128746)}
"""
with open("input.txt") as file:
    paths = file.readlines()
intersections = get_intersections(paths)
print('Closest intersection %r' % get_closest_intersection(intersections))
print('Fastest intersection %r' % get_fastest_intersection(intersections))