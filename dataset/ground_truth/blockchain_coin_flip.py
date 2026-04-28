import math
from braket.circuits import Circuit

circuit = Circuit()

circuit.h(0)
circuit.cnot(0, 1)
circuit.rz(0, math.pi / 4)
circuit.h(1)
circuit.h(0)
circuit.cnot(0, 2)
circuit.cnot(1, 2)

print(circuit)
