import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.ry(0, 2 * math.acos(0.5))
# controlled-H on q1
circuit.ry(1, math.pi / 4)
circuit.cnot(0, 1)
circuit.ry(1, -math.pi / 4)
circuit.cnot(0, 1)
circuit.ry(1, 2 * math.acos(1 / math.sqrt(2)))
circuit.cnot(1, 2)
# controlled-H on q3
circuit.ry(3, math.pi / 4)
circuit.cnot(1, 3)
circuit.ry(3, -math.pi / 4)
circuit.cnot(1, 3)
circuit.cnot(0, 1)
circuit.x(0)
