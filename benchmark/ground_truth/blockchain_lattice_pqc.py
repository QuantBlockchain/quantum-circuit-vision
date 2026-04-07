import math
from braket.circuits import Circuit

circuit = Circuit()

# H on all qubits
circuit.h(0).h(1).h(2).h(3).h(4)

# Staggered CNOT ladder with Rz + H after each
circuit.cnot(0, 1)
circuit.rz(0, math.pi / 3).h(0)

circuit.cnot(1, 2)
circuit.rz(1, math.pi / 5).h(1)

circuit.cnot(2, 3)
circuit.rz(2, math.pi / 7).h(2)

circuit.cnot(3, 4)
circuit.rz(3, math.pi / 11).h(3)
circuit.rz(4, math.pi / 13).h(4)

print(circuit)
