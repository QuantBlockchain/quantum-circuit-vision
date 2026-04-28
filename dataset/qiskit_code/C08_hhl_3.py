import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(9)
circuit.ry(math.pi / 3, 2)
circuit.h(1)
circuit.cp(math.pi / 2, 1, 2)
circuit.h(1)
# controlled Ry on ancilla
circuit.ry(math.pi / 8, 0)
circuit.cx(1, 0)
circuit.ry(-math.pi / 8, 0)
circuit.cx(1, 0)
