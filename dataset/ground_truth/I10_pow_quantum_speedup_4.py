from braket.circuits import Circuit
circuit = Circuit()
for i in range(3):
    circuit.h(i)
circuit.x(3).h(3)
circuit.ccnot(0, 1, 3).cnot(2, 3)
for i in range(3):
    circuit.h(i).x(i)
circuit.h(2).ccnot(0, 1, 2).h(2)
for i in range(3):
    circuit.x(i).h(i)
