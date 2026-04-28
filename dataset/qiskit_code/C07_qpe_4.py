import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(9)
circuit.x(3)
circuit.h(0).h(1)
circuit.cp(math.pi / 2, 0, 2).cp(math.pi / 4, 0, 3)
circuit.cp(math.pi / 4, 1, 2).cp(math.pi / 8, 1, 3)
circuit.h(0).cp(-math.pi / 2, 1, 0).h(1)
circuit.swap(0, 1)
