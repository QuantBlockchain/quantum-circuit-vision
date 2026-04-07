from braket.circuits import Circuit
circuit = Circuit()
circuit.x(0)
circuit.h(1)
circuit.x(2).h(2)
circuit.h(3)
