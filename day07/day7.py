class Amplifier:
    def __init__(self, program, input_queue=[]):
        self.memory = program.copy()
        self.input_queue = input_queue
        self.outputs = []
        self.ip = 0  # instruction pointer
        self.halted = False

    def read(self, ip, mode):
        return self.memory[self.memory[ip]] if mode == 0 else self.memory[ip]

    def write(self, ip, value):
        self.memory[self.memory[ip]] = value

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

        print(instruction,''.join(map(str,modes)))

        if instruction == 99:
            self.ip = ip
            return ("halt", None)

        elif instruction == 1:  # add
            a = self.read(ip, modes[0])
            b = self.read(ip + 1, modes[1])
            self.write(ip + 2, a + b)
            ip += 3

        elif instruction == 2:  # multiply
            a = self.read(ip, modes[0])
            b = self.read(ip + 1, modes[1])
            self.write(ip + 2, a * b)
            ip += 3

        elif instruction == 3:  # input
            if len(self.input_queue) == 0:
                self.ip = ip - 1
                # try again
                return ("wait", None)
            else:
                self.write(ip, self.input_queue.pop(0))
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
            self.write(ip + 2, 1 if a < b else 0)
            ip += 3

        elif instruction == 8:  # equals
            a = self.read(ip, modes[0])
            b = self.read(ip + 1, modes[1])
            self.write(ip + 2, 1 if a == b else 0)
            ip += 3

        self.ip = ip
        return ("ok", None)


from itertools import permutations

with open("input.txt") as file:
    program = list(map(int, file.readline().split(",")))

# PART 1

phases = [0, 1, 2, 3, 4]
max_output = 0
for phase_setting in permutations(phases):
    amps = [Amplifier(program, input_queue=[phase_setting[i]]) for i in range(5)]
    amps[0].run_until_halt([0])
    # feed output from previous amp into current amp
    for i in range(1, 5):
        amps[i].run_until_halt([amps[i - 1].outputs[-1]])
    # check if output from last amp is bigger tham max
    if amps[-1].outputs[-1] > max_output:
        max_output = amps[-1].outputs[-1]
        print(max_output, phase_setting)

# PART 2

phases = [5, 6, 7, 8, 9]
max_output = 0
for phase_setting in permutations(phases):
    # initialize amps
    amps = [Amplifier(program, input_queue=[phase_setting[i]]) for i in range(5)]
    amps[0].input_queue.append(0)  # amplifier A gets input signal 0
    # run until all amps are halted
    halted = [0] * 5
    while sum(halted) < len(halted):
        for i, amp in enumerate(amps):
            while True:
                status, value = amps[i].step()
                if status == "halt":
                    halted[i] = 1
                    break
                if status == "output":
                    output_amp = amps[(i + 1) % 5]
                    output_amp.input_queue.append(value)
                    break
                if status == "wait":
                    break  # wait for input
    # postcondition, all amps are halted, update max output
    if amps[-1].outputs[-1] > max_output:
        max_output = amps[-1].outputs[-1]
        print(max_output, phase_setting)
