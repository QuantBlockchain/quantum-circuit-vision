import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(4)
circuit.h(0).h(1)
circuit.x(3)
circuit.cx(1, 2).cx(1, 3)
circuit.ccx(0, 2, 3)
circuit.h(0).cp(-math.pi / 2, 1, 0).h(1)
