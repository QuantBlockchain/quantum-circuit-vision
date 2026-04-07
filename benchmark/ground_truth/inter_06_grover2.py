from braket.circuits import Circuit
circuit = Circuit().h(0).h(1).cz(0, 1).h(0).h(1).z(0).z(1).cz(0, 1).h(0).h(1)
