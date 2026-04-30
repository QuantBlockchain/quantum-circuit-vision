from braket.circuits import Circuit
circuit = Circuit()
circuit.x(0).x(2)
circuit.h(0).h(2)
circuit.cnot(0, 1).cnot(2, 3)
circuit.h(0).h(2)
