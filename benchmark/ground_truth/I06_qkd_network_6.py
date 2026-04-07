import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).cnot(0, 1)
circuit.h(2).cnot(2, 3)
circuit.cnot(1, 2).h(1)
circuit.ry(4, math.pi/8).ry(5, math.pi/4)
circuit.cnot(0, 4).cnot(3, 5)
