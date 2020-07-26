# Artemisia x32 Atelier

Processor based on MIPS, developed by Atelier Group.

[View this document written for Artemisia](https://docs.google.com/document/d/1sK0cbeKCon5orkNZ2AtP3siONdCbTbmgGXJhFb9fMKg/edit?usp=sharing)

[Link to Logical Circuit Simulator Library (Lucretia) GitHub](https://github.com/Atelier-Developers/Logical-Circuit-Simulator)

Utility functions that were used in the tests:

```python
def randomNBitGen(n):
    bits = ""
    for _ in range(n):
        bits += str(randint(0, 1))
    return bits

def bitsToGates(bitString, inputs):
    for i in range(len(bitString)):
        inputs[i].output = 0 if bitString[i] == "0" else 1

def set_random_value(n, input, name):
    read_gen = randomNBitGen(n)
    print(f"{name}: {read_gen}")
    bitsToGates(read_gen, input)

```

The different components used in this processor are as followed:

## ALU

Sample test code: 

```python
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
```

## Control Unit

Sample test code:

```python
def test_control_unit():
    opcodes = [Input() for _ in range(6)]

    bitsToGates("010000", opcodes)
    control_unit = ControlUnit(opcodes)
    control_unit.logic()
    outputs = control_unit.get_output()
    print("".join(map(str, outputs)))
```

## ALU Control Unit

Sample test code:

```python
def test_alu_control():
    alu_ops = [Input() for _ in range(2)]
    funct = [Input() for _ in range(6)]

    bitsToGates("01", alu_ops)
    set_random_value(6, funct, "funct")
    reg_control = ALUControlUnit(alu_ops, funct)
    reg_control.logic()
    outputs = reg_control.get_output()
    print("".join(map(str, outputs)))
```

## Forwarding Unit

Sample test code:

```python
def forward_unit_test():
    rd_ex_mem = [Input() for _ in range(5)]
    rd_mem_wb = [Input() for _ in range(5)]
    rw_ex_mem = Input()
    rw_mem_wb = Input()
    rs_id_ex = [Input() for _ in range(5)]
    rt_id_ex = [Input() for _ in range(5)]

    bitsToGates("10001", rd_ex_mem)
    bitsToGates("11101", rd_mem_wb)
    bitsToGates("10001", rs_id_ex)
    bitsToGates("11101", rt_id_ex)

    rw_ex_mem.output = 1
    rw_mem_wb.output = 1

    fu = ForwardingUnit(rd_ex_mem, rd_mem_wb, rw_ex_mem, rw_mem_wb, rs_id_ex, rt_id_ex)

    fu.logic()

    print(fu.get_output())
```

## Branch Forwarding Unit

Similar to Forwarding Unit in usage.

## Hazard Detection Unit

Sample test unit:

```python
    memread_id_ex = Input()
    rt_id_ex = [Input() for _ in range(5)]
    rt_if_id = [Input() for _ in range(5)]
    rs_if_id = [Input() for _ in range(5)]

    memread_id_ex.output = 1
    bitsToGates("10001", rt_id_ex)
    bitsToGates("10001", rt_if_id)
    bitsToGates("11001", rs_if_id)

    hdu = HazardDetectionUnit(memread_id_ex, rt_id_ex, rt_if_id, rs_if_id)
    hdu.output.logic()

    print(hdu.get_output())
```

## Main Memory

Made with four separate **Memory Banks**. The banks themselves have been made using **Memory Cells**

## Register

Registers were made using DFlipFlops from the Logical Circuit Simulator Library

## Pipeline Registers

Including PC, IF/ID, ID/EX, EX/MEM, and MEM/WB.

```python
def test_pipeline_reg():
    clock = Signal()
    inps = [Input() for _ in range(119)]
    set_random_value(119, inps, "Register inputs")
    reg = ID_EX(clock, inps)
    for _ in range(3):
        print(clock.output.output)
        output = reg.logic()
        clock.pulse()
```

## Register File 

Sample test code:

```python
def test_reg_file():
    n = 256
    reg_width = 32
    size = int(log(n, 2))
    read_num1 = [Input(f"Input{i}") for i in range(size)]
    read_num2 = [Input(f"Input{i}") for i in range(size)]
    write_num1 = [Input(f"Input{i}") for i in range(size)]
    write_val = [Input(f"Input{i}") for i in range(reg_width)]
    enable = Input()
    clock = Signal()

    reg_file = RegisterFileUnit((read_num1, read_num2, write_num1, write_val), enable, clock, n, reg_width)

    for i in range(1):
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
        print(outputs[0])
        print("".join(map(str, [outputs[0][i].output for i in range(reg_width)])))
        print("".join(map(str, [outputs[1][i].output for i in range(reg_width)])))
        clock.pulse()
```






