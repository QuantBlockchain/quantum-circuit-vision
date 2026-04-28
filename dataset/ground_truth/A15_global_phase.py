from braket.circuits import Circuit
circuit = Circuit()
circuit.s(0)
circuit.t(0)
circuit.cnot(0, 1)
circuit.ti(0)
circuit.si(0)
