from braket.circuits import Circuit
circuit = Circuit().h(0).cnot(0, 1).ccnot(0, 1, 2).h(0)
