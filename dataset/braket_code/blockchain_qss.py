import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.cnot(0, 1)
circuit.cnot(0, 2)
circuit.rz(2, math.pi / 3)
circuit.rz(1, math.pi / 4)
circuit.cnot(0, 3)
circuit.rz(3, math.pi / 6)
