from braket.circuits import Circuit
circuit = Circuit()
circuit.x(4).h(4)
for i in range(4):
    circuit.h(i)
circuit.cnot(0, 4).cnot(1, 4).cnot(3, 4)
for i in range(4):
    circuit.h(i)
