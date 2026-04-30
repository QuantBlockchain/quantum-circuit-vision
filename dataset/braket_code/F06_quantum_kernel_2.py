import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1)
circuit.rz(0, math.pi / 4).rz(1, math.pi / 3)
circuit.cnot(0, 1).rz(1, math.pi / 5).cnot(0, 1)
circuit.h(0).h(1)
