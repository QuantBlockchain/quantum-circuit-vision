import math
from braket.circuits import Circuit

circuit = Circuit()

# Layer 1: Hadamard gates
circuit.h(0).h(1).h(3).h(5)

# Layer 2: CNOT(1,2), CNOT(5,6)
circuit.cnot(1, 2).cnot(5, 6)

# Layer 3: Rz on q2, CNOT(0,1), CNOT(1,4)
circuit.rz(2, math.pi / 3).cnot(0, 1).cnot(1, 4)

# Layer 4: Rz on q4, CNOT(0,3), Rz on q6
circuit.rz(4, math.pi / 5).cnot(0, 3).rz(6, math.pi / 7)

# Layer 5: H on q1, H on q3
circuit.h(1).h(3)

# Layer 6: CNOT(0,5)
circuit.cnot(0, 5)

# Layer 7: H on q5
circuit.h(5)

print(circuit)
