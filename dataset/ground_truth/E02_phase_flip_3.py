from braket.circuits import Circuit
circuit = Circuit().cnot(0, 1).cnot(0, 2).h(0).h(1).h(2)
