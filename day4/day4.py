from collections import Counter

lower = 273025
upper = 767253

digits = '0123456789'

def is_valid_part1(s):
	return all(i <= j for i, j in zip(s, s[1:])) and any(count >= 2 for count in Counter(s).values())

def is_valid_part2(s):
	return all(i <= j for i, j in zip(s, s[1:])) and any(count == 2 for count in Counter(s).values())

valid = [n for n in range(lower, upper + 1) if is_valid_part1(str(n))]
print(valid)
print(len(valid))

valid = [n for n in range(lower, upper + 1) if is_valid_part2(str(n))]
print(valid)
print(len(valid))