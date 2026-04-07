from braket.circuits import Circuit
circuit = Circuit()
circuit.cnot(0, 1).cnot(0, 2)
circuit.cnot(3, 4).cnot(3, 5)
circuit.cnot(0, 3).cnot(1, 4).cnot(2, 5)
