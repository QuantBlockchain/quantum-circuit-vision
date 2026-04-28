import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
for i in range(5):
    circuit.h(i)
    for j in range(i + 1, 5):
        circuit.cp(math.pi / 2 ** (j - i, j, i))
circuit.swap(0, 4)
circuit.swap(1, 3)
