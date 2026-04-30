from braket.circuits import Circuit
circuit = Circuit()
circuit.x(3).h(0).h(1).h(2).h(3)
circuit.cnot(0, 3).cnot(2, 3)
circuit.h(0).h(1).h(2)
