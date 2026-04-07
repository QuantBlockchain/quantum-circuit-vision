import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(4):
    circuit.h(i)
    for j in range(i + 1, 4):
        circuit.cphaseshift(j, i, math.pi / 2 ** (j - i))
circuit.swap(0, 3)
circuit.swap(1, 2)
