import unittest


class VM:
    def __init__(self, program, inputs=[]):
        self.memory = {i: v for i, v in enumerate(program)}
        self.inputs = inputs
        self.outputs = []
        self.ip = 0  # instruction pointer
        self.relative_base = 0  # for relative mode access
        self.status = 0  # 1: halted, 2: waiting for input

    def read(self, ip, mode):
        address = -1
        if mode == 0:  # position
            address = self.memory[ip]
        elif mode == 1:  # immediate
            address = ip
        elif mode == 2:  # relative
            address = self.memory[ip] + self.relative_base
        else:
            raise ValueError(f"invalid access mode: {mode}")
        if address < 0:
            raise LookupError(f"invalid memory address: {address}")
        # default value is zero
        if address not in self.memory:
            self.memory[address] = 0
        return self.memory[address]

    def write(self, ip, value, mode=0):
        address = -1
        if mode == 0:  # position
            address = self.memory[ip]
        if mode == 1:  # immediate
            address = ip
        if mode == 2:  # relative
            address = self.memory[ip] + self.relative_base
        self.memory[address] = value

    def run(self, inputs=[]):
        self.inputs = inputs
        self.outputs = []
        while True:
            self.step()
            if self.status > 0:
                break
        return self.outputs

    def step(self):
        # decode opcode into instruction and modes
        # opcode 1203 -> instruction = 03, modes = [0, 2, 1]
        opcode = self.memory[self.ip]
        instruction = opcode % 100
        modesetting = opcode // 100
        modes = []
        for i in range(3):  # 3 is max number of params
            mode = modesetting % 10
            modes.append(mode)
            modesetting //= 10
        # print(f"{instruction:2d} {modes}")
        # run instruction and update status
        self.status = 0  # 1: halt, 2: wait for input
        if instruction == 99:  # halt
            self.status = 1
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
                self.status = 2
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
            self.ip = self.ip + 3
            if a != 0:
                self.ip = b
        elif instruction == 6:  # jump-if-false
            a = self.read(self.ip + 1, modes[0])
            b = self.read(self.ip + 2, modes[1])
            self.ip = self.ip + 3
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
        return self.status


class TestVM(unittest.TestCase):
    def test_relative_mode_quine(self):
        program = [
            109,
            1,
            204,
            -1,
            1001,
            100,
            1,
            100,
            1008,
            100,
            16,
            101,
            1006,
            101,
            0,
            99,
        ]
        correct = [
            109,
            1,
            204,
            -1,
            1001,
            100,
            1,
            100,
            1008,
            100,
            16,
            101,
            1006,
            101,
            0,
            99,
        ]
        vm = VM(program)
        outputs = vm.run()
        self.assertEqual(outputs, correct)

    def test_relative_mode_large(self):
        program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
        correct = [1219070632396864]
        vm = VM(program)
        outputs = vm.run()
        self.assertEqual(outputs, correct)

    def test_relative_mode_alloc(self):
        program = [104, 1125899906842624, 99]
        correct = [1125899906842624]
        vm = VM(program)
        outputs = vm.run()
        self.assertEqual(outputs, correct)


if __name__ == "__main__":
    unittest.main()
