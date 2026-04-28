from braket.circuits import Circuit
circuit = Circuit()
circuit.h(2)
circuit.cnot(2, 1).cnot(2, 0)
