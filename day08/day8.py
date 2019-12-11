with open("input.txt") as file:
    s = file.readline().strip()

n = 6
m = 25

nlayers = len(s) // (n * m)

# part 1

layers = []
for i in range(nlayers):
    start = i * n * m
    end = start + n * m
    layer = s[start:end]
    layers.append(list(map(int, layer)))

zeros = [layer.count(0) for layer in layers]
index = zeros.index(min(zeros))
print(layers[index].count(1) * layers[index].count(2))

# part 2

image = [2] * (n * m)  # 2 means pixel is transparent

for i in range(nlayers):
    offset = i * n * m
    for j in range(n * m):
        pixel = int(s[offset + j])
        if image[j] == 2 and (pixel == 0 or pixel == 1):
            image[j] = pixel

# print image to terminal
for i in range(n):
    for j in range(m):
        if image[i * m + j] == 1:
            print("█", end="")
        else:
            print(" ", end="")
    print("")

# plot image
import numpy as np
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt

plt.spy(np.reshape(np.array(image), (n, m)))
plt.savefig("image.png")

"""
1560
█  █  ██   ██  █  █ █  █ 
█  █ █  █ █  █ █  █ █  █ 
█  █ █    █    █  █ ████ 
█  █ █ ██ █    █  █ █  █ 
█  █ █  █ █  █ █  █ █  █ 
 ██   ███  ██   ██  █  █ 
[Finished in 0.4s]
"""
