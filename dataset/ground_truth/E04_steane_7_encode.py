from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(1).h(2)
circuit.cnot(0, 3).cnot(0, 4).cnot(0, 5)
circuit.cnot(1, 3).cnot(1, 5).cnot(1, 6)
circuit.cnot(2, 4).cnot(2, 5).cnot(2, 6)
