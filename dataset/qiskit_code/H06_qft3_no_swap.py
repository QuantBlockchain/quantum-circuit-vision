import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.h(0)
circuit.cp(math.pi / 2, 1, 0)
circuit.cp(math.pi / 4, 2, 0)
circuit.h(1)
circuit.cp(math.pi / 2, 2, 1)
circuit.h(2)
