import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(4):
    circuit.ry(i, math.pi / (i + 3))
    circuit.rz(i, math.pi / (i + 4))
for i in range(3):
    circuit.cnot(i, i + 1)
for i in range(4):
    circuit.ry(i, math.pi / (i + 5))
    circuit.rz(i, math.pi / (i + 6))
for i in range(3):
    circuit.cnot(i, i + 1)
