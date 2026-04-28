import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
for i in range(3):
    circuit.rx(math.pi / (i + 2, i))
    circuit.rz(math.pi / (i + 3, i))
circuit.cx(0, 1).cx(1, 2).cx(2, 0)
for i in range(3):
    circuit.ry(math.pi / (i + 4, i))
    circuit.rz(math.pi / (i + 5, i))
