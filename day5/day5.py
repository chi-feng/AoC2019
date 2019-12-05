num_params = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    99: 0
}

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
        modes += [0] * (num_params[instruction] - len(modes))

        if instruction == 99:
            break

        elif instruction == 1: # add
            a = memory[memory[ip]] if modes[0] == 0 else memory[ip]
            b = memory[memory[ip + 1]] if modes[1] == 0 else memory[ip + 1]
            c = memory[ip + 2]
            ip += 3
            memory[c] = a + b

        elif instruction == 2: # multiply
            a = memory[memory[ip]] if modes[0] == 0 else memory[ip]
            b = memory[memory[ip + 1]] if modes[1] == 0 else memory[ip + 1]
            c = memory[ip + 2]
            ip += 3
            memory[c] = a * b
        
        elif instruction == 3: # input
            a = memory[ip]
            ip += 1
            memory[a] = input_val

        elif instruction == 4: # output
            a = memory[memory[ip]] if modes[0] == 0 else memory[ip]
            ip += 1
            print(a)
            outputs.append(a)

        elif instruction == 5: # jump-if-true
            a = memory[memory[ip]] if modes[0] == 0 else memory[ip]
            b = memory[memory[ip + 1]] if modes[1] == 0 else memory[ip + 1]
            ip = ip + 2
            if a != 0:
                ip = b

        elif instruction == 6: # jump-if-false
            a = memory[memory[ip]] if modes[0] == 0 else memory[ip]
            b = memory[memory[ip + 1]] if modes[1] == 0 else memory[ip + 1]
            ip = ip + 2
            if a == 0:
                ip = b

        elif instruction == 7: # less than
            a = memory[memory[ip]] if modes[0] == 0 else memory[ip]
            b = memory[memory[ip + 1]] if modes[1] == 0 else memory[ip + 1]
            c = memory[ip + 2]
            ip += 3
            memory[c] = 1 if a < b else 0

        elif instruction == 8: # equals
            a = memory[memory[ip]] if modes[0] == 0 else memory[ip]
            b = memory[memory[ip + 1]] if modes[1] == 0 else memory[ip + 1]
            c = memory[ip + 2]
            ip += 3
            memory[c] = (a == b)        

    return outputs

with open("input.txt") as file:
    line = file.readline()
    tokens = line.split(",")
    memory = list(map(int, tokens))

outputs = run(memory.copy(), 1) # 13547311
outputs = run(memory.copy(), 5) # 236453
