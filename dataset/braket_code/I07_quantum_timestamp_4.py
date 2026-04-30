import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1)
circuit.cnot(0, 2).cnot(1, 3)
circuit.rz(2, math.pi/4).rz(3, math.pi/3)
circuit.h(0).h(1)
