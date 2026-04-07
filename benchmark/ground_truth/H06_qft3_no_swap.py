import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.cphaseshift(1, 0, math.pi / 2)
circuit.cphaseshift(2, 0, math.pi / 4)
circuit.h(1)
circuit.cphaseshift(2, 1, math.pi / 2)
circuit.h(2)
