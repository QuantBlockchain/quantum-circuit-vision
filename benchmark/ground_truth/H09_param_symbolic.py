from braket.circuits import Circuit
circuit = Circuit()
circuit.rx(0, 0.7)
circuit.cnot(0, 1)
circuit.ry(1, 1.2)
