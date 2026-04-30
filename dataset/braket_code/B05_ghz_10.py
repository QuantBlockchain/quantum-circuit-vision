from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
for i in range(1, 10):
    circuit.cnot(0, i)
