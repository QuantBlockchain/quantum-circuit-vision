import math
from qiskit import QuantumCircuit
circuit = QuantumCircuit(5)
circuit.ry(2 * math.acos(1 / math.sqrt(3, 0)))
# controlled-H decomposition: Ry(π/4)-CNOT-Ry(-π/4)
circuit.ry(math.pi / 4, 1)
circuit.cx(0, 1)
circuit.ry(-math.pi / 4, 1)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.cx(0, 1)
circuit.x(0)
