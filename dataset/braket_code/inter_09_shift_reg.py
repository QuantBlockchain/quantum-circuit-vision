from braket.circuits import Circuit
circuit = Circuit().x(0).cnot(0, 1).cnot(1, 2).cnot(2, 3)
