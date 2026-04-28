import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
circuit.h(0).h(1)
circuit.cx(0, 2).cx(1, 3)
circuit.ccx(0, 1, 4)
circuit.rz(math.pi/4, 2).rz(math.pi/3, 3).rz(math.pi/5, 4)
circuit.cx(2, 4).cx(3, 4)
circuit.h(4)
