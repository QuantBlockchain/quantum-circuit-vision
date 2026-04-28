import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
for i in range(4):
    circuit.h(i)
for i in range(3):
    circuit.cx(i, i + 1)
    circuit.rz(i + 1, math.pi / 4)
    circuit.cx(i, i + 1)
for i in range(4):
    circuit.h(i)
