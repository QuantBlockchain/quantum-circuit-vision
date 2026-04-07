from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1).h(2).h(3)
circuit.cnot(0, 1).cnot(2, 3)
circuit.cnot(1, 2)
circuit.h(0).h(1).h(2).h(3)
