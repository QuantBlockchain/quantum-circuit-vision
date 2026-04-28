import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.x(2)
circuit.h(0).h(1)
circuit.cp(math.pi / 2, 0, 2)
circuit.cp(math.pi / 4, 1, 2)
circuit.h(0).cp(-math.pi / 2, 1, 0).h(1)
circuit.swap(0, 1)
