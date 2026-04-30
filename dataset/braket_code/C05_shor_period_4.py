import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1)
circuit.x(3)
circuit.cnot(1, 2).cnot(1, 3)
circuit.ccnot(0, 2, 3)
circuit.h(0).cphaseshift(1, 0, -math.pi / 2).h(1)
