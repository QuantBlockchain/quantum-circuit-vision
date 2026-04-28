from braket.circuits import Circuit
circuit = Circuit()
circuit.cnot(0, 1).cnot(0, 2).cnot(0, 3).cnot(0, 4)
