import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
for layer in range(3):
    for i in range(4):
        circuit.ry(math.pi / (layer * 4 + i + 3, i))
    for i in range(3):
        circuit.cx(i, i + 1)
