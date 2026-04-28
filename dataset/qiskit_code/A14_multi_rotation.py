import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(7)
circuit.rx(math.pi / 4, 0)
circuit.ry(math.pi / 3, 0)
circuit.rz(math.pi / 6, 0)
circuit.cx(0, 1)
