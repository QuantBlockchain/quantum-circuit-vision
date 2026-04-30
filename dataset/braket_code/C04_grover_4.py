from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1)
circuit.h(1).ccnot(0, 1, 2).h(1)
circuit.h(0).h(1).x(0).x(1)
circuit.h(1).cnot(0, 1).h(1)
circuit.x(0).x(1).h(0).h(1)
