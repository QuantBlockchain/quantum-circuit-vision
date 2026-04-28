import math
from braket.circuits import Circuit
circuit = Circuit()
circuit.ry(0, 2 * math.acos(1 / math.sqrt(3)))
# controlled-H decomposition: Ry(π/4)-CNOT-Ry(-π/4)
circuit.ry(1, math.pi / 4)
circuit.cnot(0, 1)
circuit.ry(1, -math.pi / 4)
circuit.cnot(0, 1)
circuit.cnot(1, 2)
circuit.cnot(0, 1)
circuit.x(0)
