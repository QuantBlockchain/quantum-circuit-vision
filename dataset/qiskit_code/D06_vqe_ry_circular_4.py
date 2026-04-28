import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
for i in range(4):
    circuit.ry(math.pi / (i + 3, i))
for i in range(3):
    circuit.cx(i, i + 1)
circuit.cx(3, 0)
for i in range(4):
    circuit.ry(math.pi / (i + 5, i))
