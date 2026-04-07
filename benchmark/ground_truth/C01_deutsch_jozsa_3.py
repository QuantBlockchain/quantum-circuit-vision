from braket.circuits import Circuit
circuit = Circuit()
circuit.x(2).h(0).h(1).h(2)
circuit.cnot(0, 2).cnot(1, 2)
circuit.h(0).h(1)
