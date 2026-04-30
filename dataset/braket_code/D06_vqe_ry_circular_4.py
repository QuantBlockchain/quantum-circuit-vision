import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(4):
    circuit.ry(i, math.pi / (i + 3))
for i in range(3):
    circuit.cnot(i, i + 1)
circuit.cnot(3, 0)
for i in range(4):
    circuit.ry(i, math.pi / (i + 5))
