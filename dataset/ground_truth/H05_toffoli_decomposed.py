from braket.circuits import Circuit
# Toffoli decomposition into 1/2-qubit gates
circuit = Circuit()
circuit.h(2)
circuit.cnot(1, 2).ti(2).cnot(0, 2)
circuit.t(2).cnot(1, 2).ti(2).cnot(0, 2)
circuit.t(1).t(2).h(2)
circuit.cnot(0, 1).t(0).ti(1).cnot(0, 1)
