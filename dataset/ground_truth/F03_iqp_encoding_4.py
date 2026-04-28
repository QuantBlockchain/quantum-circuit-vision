import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(4):
    circuit.h(i)
for i in range(3):
    circuit.cnot(i, i + 1)
    circuit.rz(i + 1, math.pi / 4)
    circuit.cnot(i, i + 1)
for i in range(4):
    circuit.h(i)
