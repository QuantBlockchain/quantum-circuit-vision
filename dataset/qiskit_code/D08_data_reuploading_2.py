import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(7)
circuit.rx(math.pi/4, 0).rx(math.pi/5, 1)
circuit.cx(0, 1)
circuit.rx(math.pi/3, 0).rx(math.pi/6, 1)
circuit.cx(0, 1)
