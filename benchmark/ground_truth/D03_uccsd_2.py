import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.x(0)
circuit.ry(1, math.pi / 5)
circuit.cnot(0, 1)
circuit.ry(1, -math.pi / 5)
circuit.cnot(0, 1)
