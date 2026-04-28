import math
from braket.circuits import Circuit
angles = [math.pi/3, math.pi/4, math.pi/5, math.pi/6]
circuit = Circuit()
for i in range(4):
    circuit.ry(i, angles[i])
for i in range(3):
    circuit.cnot(i, i + 1)
