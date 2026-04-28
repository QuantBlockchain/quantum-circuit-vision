from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
for i in range(5):
    circuit.cnot(i, i + 1)
circuit.cnot(5, 0)
