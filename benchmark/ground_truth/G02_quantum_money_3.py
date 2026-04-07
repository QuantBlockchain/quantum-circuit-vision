from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.x(1)
circuit.h(2).s(2)
