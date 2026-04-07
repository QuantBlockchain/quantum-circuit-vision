from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.cswap(0, 1, 2)
circuit.h(0)
