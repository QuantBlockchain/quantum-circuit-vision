from braket.circuits import Circuit
# Identity gates don't change the unitary
circuit = Circuit().h(0).cnot(0, 1)
