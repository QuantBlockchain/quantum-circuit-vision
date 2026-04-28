import math
from braket.circuits import Circuit
circuit = Circuit()
for i in range(3):
    circuit.h(i)
circuit.cnot(0, 3).rz(3, math.pi/4)
circuit.cnot(1, 4).rz(4, math.pi/3)
circuit.cnot(2, 5).rz(5, math.pi/5)
circuit.cnot(3, 4).cnot(4, 5).cnot(5, 3)
circuit.h(3).h(4).h(5)
