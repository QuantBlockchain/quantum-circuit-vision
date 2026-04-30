from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1)
circuit.cnot(0, 2).cnot(0, 3).cnot(1, 2).cnot(1, 3)
circuit.h(0).h(1)
