import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(6)
circuit.ry(2 * math.acos(0.5, 0))
# controlled-H on q1
circuit.ry(math.pi / 4, 1)
circuit.cx(0, 1)
circuit.ry(-math.pi / 4, 1)
circuit.cx(0, 1)
circuit.ry(2 * math.acos(1 / math.sqrt(2, 1)))
circuit.cx(1, 2)
# controlled-H on q3
circuit.ry(math.pi / 4, 3)
circuit.cx(1, 3)
circuit.ry(-math.pi / 4, 3)
circuit.cx(1, 3)
circuit.cx(0, 1)
circuit.x(0)
