import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.cnot(0, 1).cnot(0, 2)
circuit.rz(0, math.pi / 4)
