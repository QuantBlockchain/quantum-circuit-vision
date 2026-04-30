import math
from braket.circuits import Circuit
circuit = Circuit()
for layer in range(4):
    for i in range(4):
        circuit.ry(i, math.pi * (layer * 4 + i + 1) / 17)
    for i in range(3):
        circuit.cnot(i, i + 1)
