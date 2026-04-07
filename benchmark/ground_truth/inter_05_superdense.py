from braket.circuits import Circuit
circuit = Circuit().h(0).cnot(0, 1).x(0).z(0).cnot(0, 1).h(0)
