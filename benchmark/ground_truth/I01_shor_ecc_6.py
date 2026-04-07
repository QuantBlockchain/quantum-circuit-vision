import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1).h(2)
circuit.x(5)
circuit.cnot(2, 3).cnot(2, 4)
circuit.ccnot(1, 3, 4).ccnot(1, 4, 5)
circuit.ccnot(0, 3, 5)
circuit.h(0).cphaseshift(1, 0, -math.pi/2).cphaseshift(2, 0, -math.pi/4)
circuit.h(1).cphaseshift(2, 1, -math.pi/2)
circuit.h(2)
circuit.swap(0, 2)
