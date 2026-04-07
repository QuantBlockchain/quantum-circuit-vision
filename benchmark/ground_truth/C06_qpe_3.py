import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.x(2)
circuit.h(0).h(1)
circuit.cphaseshift(0, 2, math.pi / 2)
circuit.cphaseshift(1, 2, math.pi / 4)
circuit.h(0).cphaseshift(1, 0, -math.pi / 2).h(1)
circuit.swap(0, 1)
