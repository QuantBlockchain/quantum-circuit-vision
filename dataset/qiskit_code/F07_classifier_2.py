import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(8)
circuit.rx(math.pi / 4, 0)
circuit.ry(math.pi / 3, 0).ry(math.pi / 5, 1)
circuit.cx(0, 1)
circuit.ry(math.pi / 6, 0).ry(math.pi / 7, 1)
