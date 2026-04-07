import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.x(3)
circuit.h(0).h(1)
circuit.cphaseshift(0, 2, math.pi / 2).cphaseshift(0, 3, math.pi / 4)
circuit.cphaseshift(1, 2, math.pi / 4).cphaseshift(1, 3, math.pi / 8)
circuit.h(0).cphaseshift(1, 0, -math.pi / 2).h(1)
circuit.swap(0, 1)
