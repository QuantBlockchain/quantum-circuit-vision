from braket.circuits import Circuit
circuit = Circuit()
circuit.ccnot(0, 2, 3)
circuit.cnot(0, 2)
circuit.ccnot(1, 2, 3)
