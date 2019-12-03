def run(memory):
	ip = 0
	while True:
		instruction = memory[ip]
		if instruction == 99:
			break
		(in1, in2, out) = memory[ip + 1:ip + 4]
		if instruction == 1:
			memory[out] = memory[in1] + memory[in2]
		if instruction == 2:
			memory[out] = memory[in1] * memory[in2]
		ip += 4
	return memory


# [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
print(run([1,9,10,3,2,3,11,0,99,30,40,50]))	

with open("input.txt") as file:
	line = file.readline()
	tokens = line.split(",")
	memory = list(map(int, tokens))

memory[1] = 12
memory[2] = 2

# [4576384, 12, 2, ...]
print(run(memory.copy()))


def find_inputs(memory, target):
	for noun in range(0,100):
		for verb in range(0,100):
			memory[1] = noun
			memory[2] = verb
			output = run(memory.copy())[0]
			if output == target:
				return (noun, verb)

# (12, 2)
print(find_inputs(memory, 4576384))

# (53, 98)
print(find_inputs(memory, 19690720))
