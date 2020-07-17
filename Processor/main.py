from Components.alu_unit import ALUUnit
from Components.register import Register
from Components.register_file.register_file_unit import RegisterFileUnit
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
from Components.alu import ALU
from math import log

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


def test_alu():
    n = 32
    a = [Input(f"Input{i}") for i in range(n)]
    b = [Input(f"Input{i}") for i in range(n)]
    a_gen = randomNBitGen(n)
    b_gen = randomNBitGen(n)
    print(a_gen)
    print(b_gen)
    bitsToGates(a_gen, a)
    bitsToGates(b_gen, b)
    cin = Input()
    cin.output = 0
    selector = [Input(f"Input{i}") for i in range(2)]
    bitsToGates("01", selector)
    alu = ALU(a, b, cin, selector)
    alu.logic()
    print("".join(map(str, alu.get_output())))


def test_reg_file():
    n = 8
    reg_width = 32
    size = int(log(n, 2))
    read_num1 = [Input(f"Input{i}") for i in range(size)]
    read_num2 = [Input(f"Input{i}") for i in range(size)]
    write_num1 = [Input(f"Input{i}") for i in range(size)]
    write_val = [Input(f"Input{i}") for i in range(reg_width)]
    enable = Input()
    clock = Signal()

    reg_file = RegisterFileUnit((read_num1, read_num2, write_num1, write_val), enable, clock, n, reg_width)

    for i in range(10):
        print(i)
        print("clock :" + str(clock.output.output))
        if i % 4 == 1:
            enable.output = 1
        else:
            enable.output = 0
        print("Enable Signal: " + str(enable.output))
        set_random_value(size, read_num1, "read_num1")
        set_random_value(size, read_num2, "read_num2")
        set_random_value(size, write_num1, "write_num")
        set_random_value(reg_width, write_val, "write val")
        reg_file.logic()
        outputs = reg_file.get_outputs()
        # print(outputs[0])
        print("".join(map(str, [outputs[0][i].output for i in range(reg_width)])))
        print("".join(map(str, [outputs[1][i].output for i in range(reg_width)])))
        clock.pulse()

    # Check Write as well


def set_random_value(n, input, name):
    read_gen = randomNBitGen(n)
    print(f"{name}: {read_gen}")
    bitsToGates(read_gen, input)


turn_off_debug()
test_reg_file()
# test1()