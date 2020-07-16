from Components.Register import Register
from signals.signal import Signal
from random import randint


def randomNBitGen(n):
    bits = ""
    for _ in range(n):
        bits += str(randint(0, 1))
    return bits

def test1():
    clock = Signal()
    reg1 = Register(clock, None, 32)
    for _ in range(10):
        clock.pulse()
        generated_bits = randomNBitGen(32)
        reg1.set_input(generated_bits)
        print("Generated Bits :" + generated_bits)
        print("Register Bits : " + "".join(reg1.logic()))

test1()




