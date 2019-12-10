
class Computer:
    def __init__(self, program, input_queue=[]):
        self.memory = {i: v for i, v in enumerate(program)}
        self.input_queue = input_queue
        self.outputs = []
        self.ip = 0  # instruction pointer
        self.halted = False
        self.relative_base = 0

    def read(self, ip, mode):
        address = -1
        if mode == 0:
            address = self.memory[ip]
        if mode == 1:
            address = ip
        if mode == 2:
            address = self.memory[ip] + self.relative_base
        if address not in self.memory:
            self.memory[address] = 0
        return self.memory[address]
        
    def write(self, ip, value, mode=0):
        address = -1
        if mode == 0:
            address = self.memory[ip]
        if mode == 1:
            address = ip
        if mode == 2:
            address = self.memory[ip] + self.relative_base
        self.memory[address] = value

    def run_until_halt(self, input_queue):
        self.input_queue += input_queue
        while True:
            status, value = self.step()
            if status == "halt":
                break
        return self.outputs

    def step(self):
        ip = self.ip
        # read opcode and increment pointer
        opcode = str(self.memory[ip])
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
            self.ip = ip
            return ("halt", None)

        elif instruction == 1:  # add
            a = self.read(ip, modes[0])
            b = self.read(ip + 1, modes[1])
            self.write(ip + 2, a + b, modes[2])
            ip += 3

        elif instruction == 2:  # multiply
            a = self.read(ip, modes[0])
            b = self.read(ip + 1, modes[1])
            self.write(ip + 2, a * b, modes[2])
            ip += 3

        elif instruction == 3:  # input
            if len(self.input_queue) == 0:
                self.ip = ip - 1
                # try again
                return ("wait", None)
            else:
                value = self.input_queue.pop(0)
                self.write(ip, value, modes[0])
                ip += 1

        elif instruction == 4:  # output
            output = self.read(ip, modes[0])
            ip += 1
            # print(output)
            self.outputs.append(output)
            self.ip = ip
            return ("output", output)

        elif instruction == 5:  # jump-if-true
            a = self.read(ip, modes[0])
            b = self.read(ip + 1, modes[1])
            ip = ip + 2
            if a != 0:
                ip = b

        elif instruction == 6:  # jump-if-false
            a = self.read(ip, modes[0])
            b = self.read(ip + 1, modes[1])
            ip = ip + 2
            if a == 0:
                ip = b

        elif instruction == 7:  # less than
            a = self.read(ip, modes[0])
            b = self.read(ip + 1, modes[1])
            self.write(ip + 2, 1 if a < b else 0, modes[2])
            ip += 3

        elif instruction == 8:  # equals
            a = self.read(ip, modes[0])
            b = self.read(ip + 1, modes[1])
            self.write(ip + 2, 1 if a == b else 0, modes[2])
            ip += 3

        elif instruction == 9:  # adjust relative base offset
            a = self.read(ip, modes[0])
            self.relative_base += a
            ip += 1

        self.ip = ip
        return ("ok", None)

with open("input.txt") as file:
    program = [int(token.strip()) for token in file.readline().split(",")]

c = Computer(program)
c.run_until_halt([1,])
print(c.outputs)

c = Computer(program)
c.run_until_halt([2,])
print(c.outputs)

'''
[3533056970]
[72852]
[Finished in 1.3s]
'''
