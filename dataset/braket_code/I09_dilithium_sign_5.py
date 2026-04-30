import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1)
circuit.cnot(0, 2).cnot(1, 3)
circuit.ccnot(0, 1, 4)
circuit.rz(2, math.pi/4).rz(3, math.pi/3).rz(4, math.pi/5)
circuit.cnot(2, 4).cnot(3, 4)
circuit.h(4)
