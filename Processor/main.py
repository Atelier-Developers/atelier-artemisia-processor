from Components.alu.left_shift import LeftSift
from Components.forwading_unit.forwarding_unit import ForwardingUnit
from Components.hazard_detection_unit.hazard_detection_unit import HazardDetectionUnit
from Components.register_file.register import Register
from Components.register_file.register_file_unit import RegisterFileUnit
from Components.alu.right_shift import RightSift
from Components.sign_extend.sign_extend_16to32 import SignExtend16To32
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
from Components.alu.alu import ALU
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
    shamt = [Input(f"Input{i}") for i in range(5)]
    a_gen = randomNBitGen(n)
    b_gen = randomNBitGen(n)
    shamt_gen = randomNBitGen(5)
    print("a_gen: " + a_gen)
    print("b_gen: " + b_gen)
    print("shamt_gen: " + shamt_gen)
    bitsToGates(a_gen, a)
    bitsToGates(b_gen, b)
    bitsToGates(shamt_gen, shamt)
    cin = Input()
    cin.output = 0
    selector = [Input(f"Input{i}") for i in range(4)]
    bitsToGates("0100", selector)
    alu = ALU(a, b, cin, selector, shamt)
    alu.logic()
    print("xxxxx: " + "".join(map(str, alu.get_output())))


def test_reg_file():
    n = 4
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


def test_right_shift():
    a = [Input(f"Input{i}") for i in range(32)]
    b = [Input(f"Input{i}") for i in range(5)]
    set_random_value(32, a, "a")
    bitsToGates("00011", b)
    right_shift = RightSift(a, b, 32)
    right_shift.logic()
    print("".join(map(str, [right_shift.get_output()[i] for i in range(32)])))


def test_left_shift():
    a = [Input(f"Input{i}") for i in range(32)]
    b = [Input(f"Input{i}") for i in range(5)]
    set_random_value(32, a, "a")
    bitsToGates("00011", b)
    left_shift = LeftSift(a, b, 32)
    left_shift.logic()
    print("".join(map(str, [left_shift.get_output()[i] for i in range(32)])))


def set_random_value(n, input, name):
    read_gen = randomNBitGen(n)
    print(f"{name}: {read_gen}")
    bitsToGates(read_gen, input)


def test_sign_extend():
    a = [Input(f"Input{i}") for i in range(16)]
    set_random_value(16, a, "a")
    sign_extend = SignExtend16To32(a)
    sign_extend.logic()
    print("".join(map(str, [sign_extend.get_output()[i] for i in range(32)])))


def forward_unit_test():
    rd_ex_mem = [Input() for _ in range(5)]
    rd_mem_wb = [Input() for _ in range(5)]
    rw_ex_mem = Input()
    rw_mem_wb = Input()
    rs_id_ex = [Input() for _ in range(5)]
    rt_id_ex = [Input() for _ in range(5)]

    bitsToGates("11101", rd_ex_mem)
    bitsToGates("10001", rd_mem_wb)
    bitsToGates("11101", rs_id_ex)
    bitsToGates("11001", rt_id_ex)

    rw_ex_mem.output = 1
    rw_mem_wb.output = 1

    fu = ForwardingUnit(rd_ex_mem, rd_mem_wb, rw_ex_mem, rw_mem_wb, rs_id_ex, rt_id_ex)

    fu.outputs[0][0].logic()
    fu.outputs[0][1].logic()
    fu.outputs[1][0].logic()
    fu.outputs[1][1].logic()

    print(fu.outputs)


def hazard_test():
    rm_id_ex = Input()
    rt_id_ex = [Input() for _ in range(5)]
    rt_if_id = [Input() for _ in range(5)]
    rs_if_id = [Input() for _ in range(5)]

    rm_id_ex.output = 0
    bitsToGates("10001", rt_id_ex)
    bitsToGates("11001", rt_if_id)
    bitsToGates("10001", rs_if_id)

    hdu = HazardDetectionUnit(rm_id_ex, rt_id_ex, rt_if_id, rs_if_id)
    hdu.output.logic()

    print(hdu.output)


# turn_off_debug()
# test_right_shift()
# test_left_shift()
# test_sign_extend()
# test_reg_file()
# test1()
# test_alu()
# forward_unit_test()

# hazard_test()
