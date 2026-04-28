import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(8)
for i in range(0, 8, 2):
    circuit.ry(math.pi / 4, i)
    circuit.ry(i + 1, math.pi / 4)
    circuit.cx(i, i + 1)
for i in range(0, 8, 2):
    circuit.cx(i, i + 1)
circuit.ry(math.pi / 3, 1).ry(math.pi / 3, 3).cx(1, 3)
circuit.ry(math.pi / 3, 5).ry(math.pi / 3, 7).cx(5, 7)
circuit.cx(1, 3).cx(5, 7)
