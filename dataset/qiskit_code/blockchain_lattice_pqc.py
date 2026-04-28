import math
from qiskit import QuantumCircuit

circuit = QuantumCircuit(14)

# H on all qubits
circuit.h(0).h(1).h(2).h(3).h(4)

# Staggered CNOT ladder with Rz + H after each
circuit.cx(0, 1)
circuit.rz(math.pi / 3, 0).h(0)

circuit.cx(1, 2)
circuit.rz(math.pi / 5, 1).h(1)

circuit.cx(2, 3)
circuit.rz(math.pi / 7, 2).h(2)

circuit.cx(3, 4)
circuit.rz(math.pi / 11, 3).h(3)
circuit.rz(math.pi / 13, 4).h(4)

print(circuit)
