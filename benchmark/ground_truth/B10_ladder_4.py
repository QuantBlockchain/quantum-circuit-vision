from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.cnot(0, 1)
circuit.cnot(1, 2)
circuit.cnot(2, 3)
circuit.cnot(3, 0)
