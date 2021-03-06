class VM:
    def __init__(self):
        pass

    def load(self, program):
        self.memory = {i: v for i, v in enumerate(program)}
        self.ip = 0  # reset instruction pointer
        self.relative_base = 0  # for relative mode access
        self.OKAY = 0
        self.HALT = 1
        self.WAIT = 2
        self.status = self.OKAY
        self.inputs = []
        self.outputs = []

    def load_file(self, filename):
        with open(filename, "r") as f:
            program = map(int, f.readline().strip().split(","))
            self.load(program)

    def copy(self):
        vm = VM()
        vm.load([])
        vm.memory = self.memory.copy()
        vm.ip = self.ip
        vm.relative_base = self.relative_base
        vm.status = self.status
        vm.inputs = self.inputs.copy()
        vm.outputs = self.outputs.copy()
        return vm

    def read(self, ip, mode):
        address = -1
        if mode == 0:  # position
            address = self.memory[ip]
        elif mode == 1:  # immediate
            address = ip
        elif mode == 2:  # relative
            address = self.memory[ip] + self.relative_base
        else:
            raise ValueError(f"invalid address mode: {mode}")
        if address < 0:
            raise LookupError(f"invalid memory address: {address}")
        # default value is zero
        return self.memory.get(address, 0)

    def write(self, ip, value, mode=0):
        address = -1
        if mode == 0:  # position
            address = self.memory[ip]
        elif mode == 1:  # immediate
            address = ip
        elif mode == 2:  # relative
            address = self.memory[ip] + self.relative_base
        else:
            raise ValueError(f"invalid address mode: {mode}")
        if address < 0:
            raise LookupError(f"invalid memory address: {address}")
        self.memory[address] = value

    def run(self, inputs=[]):
        if inputs:
            self.inputs = inputs
        while True:
            if self.step() != self.OKAY:
                break
        return self.outputs

    def step(self):
        # decode opcode into instruction and modes
        # opcode 1203 -> instruction = 03, modes = [0, 2, 1]
        opcode = self.memory[self.ip]
        instruction = opcode % 100
        modesetting = opcode // 100
        modes = [0] * 3
        for i in range(3):  # 3 is max number of params
            mode = modesetting % 10
            modes[i] = mode
            modesetting //= 10

        self.status = self.OKAY  # 1: halt, 2: wait for input
        if instruction == 99:  # halt
            self.status = self.HALT
        elif instruction == 1:  # add
            a = self.read(self.ip + 1, modes[0])
            b = self.read(self.ip + 2, modes[1])
            self.write(self.ip + 3, a + b, modes[2])
            self.ip += 4
        elif instruction == 2:  # multiply
            a = self.read(self.ip + 1, modes[0])
            b = self.read(self.ip + 2, modes[1])
            self.write(self.ip + 3, a * b, modes[2])
            self.ip += 4
        elif instruction == 3:  # input
            if len(self.inputs) == 0:  # ran out of inputs!
                self.status = self.WAIT
            else:
                value = self.inputs.pop(0)
                self.write(self.ip + 1, value, modes[0])
                self.ip += 2
        elif instruction == 4:  # output
            output = self.read(self.ip + 1, modes[0])
            self.outputs.append(output)
            self.ip += 2
        elif instruction == 5:  # jump-if-true
            a = self.read(self.ip + 1, modes[0])
            b = self.read(self.ip + 2, modes[1])
            self.ip += 3
            if a != 0:
                self.ip = b
        elif instruction == 6:  # jump-if-false
            a = self.read(self.ip + 1, modes[0])
            b = self.read(self.ip + 2, modes[1])
            self.ip += 3
            if a == 0:
                self.ip = b
        elif instruction == 7:  # less than
            a = self.read(self.ip + 1, modes[0])
            b = self.read(self.ip + 2, modes[1])
            self.write(self.ip + 3, 1 if a < b else 0, modes[2])
            self.ip += 4
        elif instruction == 8:  # equals
            a = self.read(self.ip + 1, modes[0])
            b = self.read(self.ip + 2, modes[1])
            self.write(self.ip + 3, 1 if a == b else 0, modes[2])
            self.ip += 4
        elif instruction == 9:  # adjust relative base offset
            a = self.read(self.ip + 1, modes[0])
            self.relative_base += a
            self.ip += 2
        else:
            raise ValueError(f"invalid instruction: {instruction}")
        return self.status
