lower = 273025
upper = 767253

digits = '0123456789'

def is_valid_part1(s):
	# non decreasing
	if any(s[i] < s[i-1] for i in range(1, len(s))):
		return False
	# contains the same digit (at least) twice
	return any(2 * d in s for d in digits)

def is_valid_part2(s):
	# non decreasing
	if any(s[i] < s[i-1] for i in range(1, len(s))):
		return False
	# contains the same digit twice, but not three (or more) times
	return any(2 * d in s and 3 * d not in s for d in digits)

valid = [number for number in range(lower, upper + 1) if is_valid_part1(str(number))]
# print(valid)
print(len(valid))

valid = [number for number in range(lower, upper + 1) if is_valid_part2(str(number))]
# print(valid)
print(len(valid))