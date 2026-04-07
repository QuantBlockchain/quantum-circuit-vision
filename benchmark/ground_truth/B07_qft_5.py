import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(5):
    circuit.h(i)
    for j in range(i + 1, 5):
        circuit.cphaseshift(j, i, math.pi / 2 ** (j - i))
circuit.swap(0, 4)
circuit.swap(1, 3)
