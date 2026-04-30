import math
from braket.circuits import Circuit

circuit = Circuit()

# Layer 1: H gates
circuit.h([0, 2, 4, 6])

# Layer 2: CNOT pairs
circuit.cnot(0, 1).cnot(2, 3).cnot(4, 5).cnot(6, 7)

# Layer 3: CNOT chain
circuit.cnot(1, 2).cnot(3, 4).cnot(5, 6)

# Layer 4: CNOT wrap-around
circuit.cnot(7, 0)

# Layer 5: Rz(pi/4)
circuit.rz([0, 2, 4, 6], math.pi / 4)

# Layer 6: H gates
circuit.h([0, 2, 4, 6])

print(circuit)
