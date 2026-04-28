import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(8)
circuit.ry(math.pi / 3, 0)
circuit.cx(0, 1)
circuit.ry(math.pi / 5, 1)
circuit.cx(0, 1)
circuit.ry(math.pi / 7, 1)
