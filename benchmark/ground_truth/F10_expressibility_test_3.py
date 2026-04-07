import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(3):
    circuit.rx(i, math.pi / (i + 2))
    circuit.rz(i, math.pi / (i + 3))
circuit.cnot(0, 1).cnot(1, 2).cnot(2, 0)
for i in range(3):
    circuit.ry(i, math.pi / (i + 4))
    circuit.rz(i, math.pi / (i + 5))
