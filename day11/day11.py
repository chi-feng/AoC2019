program = list(map(int, open("input.txt").readline().strip().split(',')))


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

    def run_until_input(self, input_queue):
        self.input_queue = input_queue
        self.outputs = []
        while True:
            status, value = self.step()
            if status == "halt":
                break
            if status == "wait":
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
            self.halted = True
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

class Robot:

    def __init__(self, program):
        self.program = program;
        self.computer = Computer(program)
        self.direction = 0; # north
        self.dxdy = {0:(0,1),1:(1,0),2:(0,-1),3:(-1,0)}
        self.x = 0
        self.y = 0

    def send_color(self, c):
        outputs = self.computer.run_until_input([c])
        return outputs

    def turn_left(self):
        self.direction -= 1
        if self.direction == -1:
            self.direction = 3

    def turn_right(self):
        self.direction += 1
        if self.direction == 4:
            self.direction = 0

    def move(self):
        dx, dy = self.dxdy[self.direction]
        self.x += dx
        self.y += dy

r = Robot(program)

colors = dict()
colors[(0,0)] = 1;

painted_panels = set();

while True:

    color = colors.get((r.x, r.y), 0)

    print('robot at', (r.x, r.y), end=' ')

    outputs = r.send_color(color)
    paint_color, direction = outputs[0], outputs[1]
    
    print('paint', color, '->', paint_color)

    colors[(r.x, r.y)] = paint_color

    if color != paint_color:
        painted_panels.add((r.x, r.y))

    if direction == 0:
        r.turn_left()
    if direction == 1:
        r.turn_right()
    r.move()

    if r.computer.halted:
        break

print(len(painted_panels))

import matplotlib 
matplotlib.use('Agg')
from matplotlib import pyplot as plt

white = [k for k,v in colors.items() if v == 1]
x,y=zip(*white)
plt.figure(figsize=(4,0.6))
plt.plot(x,y, 'ko')

plt.savefig('output.png')






