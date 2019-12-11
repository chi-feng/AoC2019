import sys

sys.path.append("../")

from shared.intcode import VM

with open("input.txt") as file:
    program = [int(token.strip()) for token in file.readline().split(",")]

vm = VM(program)
vm.run([1])
print(vm.outputs)

vm = VM(program)
vm.run([2])
print(vm.outputs)

"""
[3533056970]
[72852]
[Finished in 1.3s]
"""
