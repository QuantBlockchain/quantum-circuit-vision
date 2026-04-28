import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.h(0)
for i in range(1, 5):
    circuit.cx(0, i)
circuit.rz(math.pi / 4, 1).rz(math.pi / 4, 3)
circuit.h(0)
