import math
from qiskit import QuantumCircuit
# CCRz(π/4) decomposed
circuit = QuantumCircuit(9)
circuit.cx(1, 2)
circuit.rz(-math.pi / 8, 2)
circuit.cx(0, 2)
circuit.rz(math.pi / 8, 2)
circuit.cx(1, 2)
circuit.rz(-math.pi / 8, 2)
circuit.cx(0, 2)
circuit.rz(math.pi / 8, 2)
