from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
for i in range(1, 8):
    circuit.cnot(0, i)
