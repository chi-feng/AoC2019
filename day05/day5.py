def read(memory, ip, mode):
    return memory[memory[ip]] if mode == 0 else memory[ip]


def write(memory, ip, value):
    address = memory[ip]
    memory[address] = value


def run(memory, input_val):

    outputs = []

    ip = 0

    while True:

        # read opcode and increment pointer
        opcode = memory[ip]
        ip += 1

        # opcode 1203 -> instruction = 03, modes = [0, 2, 1]
        instruction = opcode % 100
        modesetting = opcode // 100
        modes = []
        for _ in range(3):  # 3 is max number of params
            mode = modesetting % 10
            modes.append(mode)
            modesetting //= 10

        if instruction == 99:
            break

        elif instruction == 1:  # add
            a = read(memory, ip, modes[0])
            b = read(memory, ip + 1, modes[1])
            write(memory, ip + 2, a + b)
            ip += 3

        elif instruction == 2:  # multiply
            a = read(memory, ip, modes[0])
            b = read(memory, ip + 1, modes[1])
            write(memory, ip + 2, a * b)
            ip += 3

        elif instruction == 3:  # input
            write(memory, ip, input_val)
            ip += 1

        elif instruction == 4:  # output
            output = read(memory, ip, modes[0])
            ip += 1
            print(output)
            outputs.append(output)

        elif instruction == 5:  # jump-if-true
            a = read(memory, ip, modes[0])
            b = read(memory, ip + 1, modes[1])
            ip = ip + 2
            if a != 0:
                ip = b

        elif instruction == 6:  # jump-if-false
            a = read(memory, ip, modes[0])
            b = read(memory, ip + 1, modes[1])
            ip = ip + 2
            if a == 0:
                ip = b

        elif instruction == 7:  # less than
            a = read(memory, ip, modes[0])
            b = read(memory, ip + 1, modes[1])
            write(memory, ip + 2, 1 if a < b else 0)
            ip += 3

        elif instruction == 8:  # equals
            a = read(memory, ip, modes[0])
            b = read(memory, ip + 1, modes[1])
            write(memory, ip + 2, 1 if a == b else 0)
            ip += 3

    return outputs


with open("input.txt") as file:
    line = file.readline()
    tokens = line.split(",")
    memory = list(map(int, tokens))

outputs = run(memory.copy(), 1)  # 13547311
outputs = run(memory.copy(), 5)  # 236453
