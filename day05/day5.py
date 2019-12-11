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
        opcode = str(memory[ip])
        ip += 1

        # get instruction and modes and from opcode
        instruction = int(opcode)
        modes = []
        if len(opcode) >= 2:
            instruction = int(opcode[-2:])
            # Parameter modes are single digits, one per parameter, read right-to-left from the opcode
            modes = list(map(int, opcode[::-1][2:]))
        # Any missing modes are 0 by default.
        modes += [0] * (4 - len(modes))

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
