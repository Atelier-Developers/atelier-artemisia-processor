from gate.input_gate import Input


def bits_to_gates(bitstring, inps):
    for i in range(len(bitstring)):
        inps[i].output = 0 if bitstring[i] == "0" else 1
    return inps
