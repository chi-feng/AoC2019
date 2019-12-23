import os
import sys

sys.path.append("../")
from shared import intcode


def init_vms():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "input.txt")
    vm = intcode.VM()
    vm.load_file(filename)
    vms = [vm.copy() for i in range(50)]
    for i, vm in enumerate(vms):
        vm.inputs.append(i)
        vm.run()
    return vms


def part1():
    vms = init_vms()
    while True:
        for vm in vms:
            if not vm.inputs:
                vm.inputs.append(-1)
            vm.run()
            while vm.outputs:
                a = vm.outputs.pop(0)
                x = vm.outputs.pop(0)
                y = vm.outputs.pop(0)
                if a == 255:
                    return y
                else:
                    vms[a].inputs.extend([x, y])


def part2():
    vms = init_vms()
    natx = None
    naty = None
    lastnaty = None
    while True:
        idle = True
        for vm in vms:
            if not vm.inputs:
                vm.inputs.append(-1)
            else:
                idle = False
            vm.run()
            while vm.outputs:
                a = vm.outputs.pop(0)
                x = vm.outputs.pop(0)
                y = vm.outputs.pop(0)
                if a == 255:
                    natx = x
                    naty = y
                else:
                    vms[a].inputs.extend([x, y])
        if idle and natx is not None and naty is not None:
            if naty == lastnaty:
                return naty
            vms[0].inputs.extend([natx, naty])
            lastnaty = naty


print(part1())
print(part2())
