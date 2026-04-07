import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
for i in range(1, 5):
    circuit.cnot(0, i)
circuit.rz(1, math.pi / 4).rz(3, math.pi / 4)
circuit.h(0)
