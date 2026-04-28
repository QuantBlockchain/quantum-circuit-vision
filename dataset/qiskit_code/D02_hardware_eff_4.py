import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(7)
for i in range(4):
    circuit.ry(math.pi / (i + 3, i))
    circuit.rz(math.pi / (i + 4, i))
for i in range(3):
    circuit.cx(i, i + 1)
for i in range(4):
    circuit.ry(math.pi / (i + 5, i))
    circuit.rz(math.pi / (i + 6, i))
for i in range(3):
    circuit.cx(i, i + 1)
