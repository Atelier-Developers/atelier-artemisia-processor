from Components.Register import Register
from flipflop.d import D_FlipFlop
from gate.and_gate import And
from gate.input_gate import Input
from gate.not_gate import Not
from gate.or_gate import Or
from gate.xor_gate import Xor
from latch.d import D_Latch
from multiplexer.mux2x1 import Mux2x1
from multiplexer.mux4x2 import Mux4x2
from signals.signal import Signal

from random import randint


def turn_off_debug(every_thing=False):
    And.DEBUGMODE = every_thing
    Or.DEBUGMODE = every_thing
    Xor.DEBUGMODE = every_thing
    D_FlipFlop.DEBUGMODE = every_thing
    D_Latch.DEBUGMODE = every_thing
    Not.DEBUGMODE = every_thing
    Mux2x1.DEBUGMODE = every_thing
    Mux4x2.DEBUGMODE = every_thing
    Signal.DEBUGMODE = every_thing
    Register.DEBUGMODE = every_thing


def randomNBitGen(n):
    bits = ""
    for _ in range(n):
        bits += str(randint(0, 1))
    return bits


def bitsToGates(bitString, inputs):
    for i in range(len(bitString)):
        inputs[i].output = 0 if bitString[i] == "0" else 1


def test1():
    clock = Signal()
    inputs = [Input(f"Input{i}") for i in range(32)]
    reg1 = Register(clock, inputs, 32)

    outputs = []
    for __ in range(10):
        generated_bits = randomNBitGen(32)
        bitsToGates(generated_bits, inputs)
        for _ in range(1):
            print(clock.output.output)
            outputs = reg1.logic()
            clock.pulse()
        print("Generated Bits :" + generated_bits)
        print("Register Bits : " + "".join(map(str, outputs)))


turn_off_debug()
test1()
