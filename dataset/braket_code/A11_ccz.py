from braket.circuits import Circuit
# CCZ = H(2)-CCX-H(2)
circuit = Circuit()
circuit.h(2)
circuit.ccnot(0, 1, 2)
circuit.h(2)
