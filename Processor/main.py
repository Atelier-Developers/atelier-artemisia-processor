from Components.Register import Register
from signals.signal import Signal
from random import randint
from gate import one_gate, zero_gate


def randomNBitGen(n):
    bits = ""
    for _ in range(n):
        bits += str(randint(0, 1))
    return bits

def bitsToGates(bitString):
    gates = []
    for bit in bitString:
        if bit == "0":
            gates.append(zero_gate.Zero())
        elif bit == "1":
            gates.append(one_gate.One())
    return gates


def test1():
    clock = Signal()
    reg1 = Register(clock, None, 32)

    outputs = []
    for __ in range(10):
        generated_bits = randomNBitGen(32)
        gates = bitsToGates(generated_bits)
        reg1.set_input(gates)
        for _ in range(1):
            print(clock.output.output)
            outputs = reg1.logic()
            clock.pulse()
        print("Generated Bits :" + generated_bits)
        print("Register Bits : " + "".join(map(str, outputs)))

test1()




