from braket.circuits import Circuit
circuit = Circuit().x(1).h(0).h(1).cnot(0, 1).h(0)
