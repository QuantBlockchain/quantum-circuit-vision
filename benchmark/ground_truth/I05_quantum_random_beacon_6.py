import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).cnot(0, 2).cnot(0, 4)
circuit.rz(1, math.pi/3).rz(3, math.pi/5).rz(5, math.pi/7)
circuit.cnot(0, 1).cnot(2, 3).cnot(4, 5)
circuit.h(0).h(2).h(4)
