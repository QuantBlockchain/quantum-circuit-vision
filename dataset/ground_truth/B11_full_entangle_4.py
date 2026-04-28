from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
for i in range(4):
    for j in range(i + 1, 4):
        circuit.cnot(i, j)
