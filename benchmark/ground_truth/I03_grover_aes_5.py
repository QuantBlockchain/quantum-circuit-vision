from braket.circuits import Circuit
circuit = Circuit()
for i in range(4):
    circuit.h(i)
circuit.x(4).h(4)
circuit.cnot(0, 4).cnot(1, 4).ccnot(2, 3, 4)
for i in range(4):
    circuit.h(i)
for i in range(4):
    circuit.x(i)
circuit.h(3).ccnot(0, 1, 2).cnot(2, 3).h(3)
for i in range(4):
    circuit.x(i)
for i in range(4):
    circuit.h(i)
