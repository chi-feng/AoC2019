parent_of = dict()
with open("input.txt") as file:
	for line in file.readlines():
		tokens = line.strip().split(')')
		parent_of[tokens[1]] = tokens[0]

planets = set(parent_of.keys()) | set(parent_of.values())

def get_orbits(planet):
	orbits = []
	while planet != 'COM':
		orbits.append(parent_of[planet])
		planet = parent_of[planet]
	return orbits

orbit_count = 0
for planet in planets:
	orbits = get_orbits(planet)
	orbit_count += len(orbits)

print(orbit_count)

my_orbits = get_orbits('YOU')
santa_orbits = get_orbits('SAN')
common_ancestors = set(my_orbits) & set(santa_orbits)
min_transfers = min(my_orbits.index(ancestor) + santa_orbits.index(ancestor) for ancestor in common_ancestors)
print(min_transfers)
