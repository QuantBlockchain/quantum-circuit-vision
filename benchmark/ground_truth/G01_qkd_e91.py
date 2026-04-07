import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).cnot(0, 1)
circuit.h(2).cnot(2, 3)
circuit.ry(0, math.pi / 8)
circuit.ry(1, math.pi / 4)
