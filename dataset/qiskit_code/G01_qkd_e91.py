import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(9)
circuit.h(0).cx(0, 1)
circuit.h(2).cx(2, 3)
circuit.ry(math.pi / 8, 0)
circuit.ry(math.pi / 4, 1)
