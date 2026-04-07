import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(4):
    circuit.h(i)
circuit.cnot(0, 4).cnot(1, 4).rz(4, math.pi/4)
circuit.cnot(2, 5).cnot(3, 5).rz(5, math.pi/3)
circuit.cnot(4, 6).cnot(5, 6)
circuit.h(6)
circuit.ccnot(4, 5, 6)
circuit.rz(6, math.pi/5)
