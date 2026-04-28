import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(7)
circuit.h(0).h(1).h(2)
circuit.ry(math.pi / 4, 0).ry(math.pi / 5, 1).ry(math.pi / 6, 2)
circuit.cx(0, 1).cx(1, 2)
circuit.ry(math.pi / 3, 0).ry(math.pi / 4, 1).ry(math.pi / 5, 2)
