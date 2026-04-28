import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
for i in range(4):
    circuit.h(i)
    for j in range(i + 1, 4):
        circuit.cp(math.pi / 2 ** (j - i, j, i))
circuit.swap(0, 3)
circuit.swap(1, 2)
