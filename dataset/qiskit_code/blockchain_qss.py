import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(7)
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(0, 2)
circuit.rz(math.pi / 3, 2)
circuit.rz(math.pi / 4, 1)
circuit.cx(0, 3)
circuit.rz(math.pi / 6, 3)
