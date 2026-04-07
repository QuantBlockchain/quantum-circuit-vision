from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1).h(2)
circuit.h(2).ccnot(0, 1, 2).h(2)
circuit.h(0).h(1).h(2)
circuit.x(0).x(1).x(2)
circuit.h(2).ccnot(0, 1, 2).h(2)
circuit.x(0).x(1).x(2)
circuit.h(0).h(1).h(2)
