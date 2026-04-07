from braket.circuits import Circuit
circuit = Circuit()
circuit.h(4).cnot(4, 0).cnot(4, 1).h(4)
circuit.h(5).cnot(5, 2).cnot(5, 3).h(5)
circuit.cnot(0, 6).cnot(2, 6)
circuit.cnot(1, 7).cnot(3, 7)
circuit.cnot(0, 8).cnot(1, 8)
