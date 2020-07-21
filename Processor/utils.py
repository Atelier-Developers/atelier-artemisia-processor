from gate.input_gate import Input


def bits_to_gates(bitstring):
    inputs = [Input() for _ in range(len(bitstring))]
    for i in range(len(bitstring)):
        inputs[i].output = 0 if bitstring[i] == "0" else 1
    return inputs
