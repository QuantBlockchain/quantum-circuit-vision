import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
circuit.h(0).h(1).h(2)
circuit.x(5)
circuit.cx(2, 3).cx(2, 4)
circuit.ccx(1, 3, 4).ccx(1, 4, 5)
circuit.ccx(0, 3, 5)
circuit.h(0).cp(-math.pi/2, 1, 0).cp(-math.pi/4, 2, 0)
circuit.h(1).cp(-math.pi/2, 2, 1)
circuit.h(2)
circuit.swap(0, 2)
