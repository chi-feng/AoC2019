with open("input.txt") as file:
	masses = [int(line) for line in file.readlines()]

# 3303995
print(sum(map(lambda m: m // 3 - 2, masses)))

def fuel_requirement(mass):
	fuel = mass // 3 - 2
	total = fuel
	while fuel > 0:
		fuel = fuel // 3 - 2
		if fuel > 0:
			total += fuel
	return total

# 4953118
print(sum(map(fuel_requirement, masses)))

