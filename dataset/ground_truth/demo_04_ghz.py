from braket.circuits import Circuit
circuit = Circuit().h(0).cnot(0, 1).cnot(0, 2)
