from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0).h(2)
circuit.cnot(0, 1).cnot(2, 3)
circuit.cnot(1, 4).cnot(3, 4)
circuit.h(4)
circuit.ccnot(0, 2, 4)
