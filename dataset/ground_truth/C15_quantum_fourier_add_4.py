import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).cphaseshift(1, 0, math.pi / 2)
circuit.h(1)
circuit.cphaseshift(2, 0, math.pi / 2).cphaseshift(3, 0, math.pi / 4)
circuit.cphaseshift(3, 1, math.pi / 2)
circuit.h(1).cphaseshift(1, 0, -math.pi / 2).h(0)
