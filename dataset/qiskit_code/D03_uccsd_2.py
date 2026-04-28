import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
circuit.x(0)
circuit.ry(math.pi / 5, 1)
circuit.cx(0, 1)
circuit.ry(-math.pi / 5, 1)
circuit.cx(0, 1)
