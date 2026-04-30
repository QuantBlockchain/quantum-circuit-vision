import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(0, 8, 2):
    circuit.ry(i, math.pi / 4)
    circuit.ry(i + 1, math.pi / 4)
    circuit.cnot(i, i + 1)
for i in range(0, 8, 2):
    circuit.cnot(i, i + 1)
circuit.ry(1, math.pi / 3).ry(3, math.pi / 3).cnot(1, 3)
circuit.ry(5, math.pi / 3).ry(7, math.pi / 3).cnot(5, 7)
circuit.cnot(1, 3).cnot(5, 7)
