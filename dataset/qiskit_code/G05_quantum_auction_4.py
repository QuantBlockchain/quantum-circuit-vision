import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(7)
circuit.ry(math.pi/3, 0).ry(math.pi/4, 1).ry(math.pi/5, 2).ry(math.pi/6, 3)
circuit.cx(0, 2).cx(1, 3)
circuit.ccx(2, 3, 0)
