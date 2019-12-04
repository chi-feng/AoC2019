from collections import Counter

lower = 273025
upper = 767253

def is_valid1(s):
	return list(s) == sorted(s) and any(count >= 2 for count in Counter(s).values())

def is_valid2(s):
	return list(s) == sorted(s) and any(count == 2 for count in Counter(s).values())

print(sum(1 for n in range(lower, upper) if is_valid1(str(n))))
print(sum(1 for n in range(lower, upper) if is_valid2(str(n))))
