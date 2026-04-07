from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).cnot(0, 1)
circuit.h(2).cnot(2, 3)
circuit.cnot(1, 2)
circuit.h(1)
