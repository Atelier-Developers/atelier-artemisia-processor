import re

j_format = {
    "j": "000010",
}
i_format = {
    'beq': "000100",
    'bne': None,
    'addi': "001000",
    'addiu': None,
    'andi': None,
    'ori': None,
    'slti': None,
    'sltiu': None,
    'lui': None,
    'lw': "100011",
    'sw': "101011",
}

r_format = {
    'add': "100000",
    'addu': None,
    'sub': "100010",
    'subu': None,
    'and': "100100",
    'or': "100101",
    'xor': "100110",
    'slt': "101010",
    'sltu': None,
    'sll': "101001",
    'srl': None,
    'jr': None
}
reg_name = {
    '$zero': 1,
    '$at': 1,
    '$v': 2,
    '$a': 4,
    '$t': 8,
    '$s': 8,
    '$tt': 2,
    '$k': 2,
    '$gp': 1,
    '$sp': 1,
    '$fp': 1,
    '$ra': 1
}


def reg_init():
    registers = {}
    n = 0
    for key, value in reg_name.items():
        for i in range(value):
            b = bin(n)[2:].zfill(5)
            if key == "$zero":
                registers[f"{key}"] = b
            elif key == "$tt":
                registers[f"$t{i + 8}"] = b
            else:
                registers[f"{key}{i}"] = b
            n += 1
    return registers


def check_dependency(ins, regs):
    if ins[1] in regs:
        return True
    return False


def twos_comp(binary):
    binary = binary[::-1]
    new_b = ""
    flag = False
    for i in range(len(binary)):
        if flag:
            new_b += '0' if binary[i] == '1' else '1'
        else:
            if binary[i] == '1':
                flag = True
            new_b += binary[i]
    return new_b[::-1]


def compile_asm(lines, registers):
    # for beq, if R -> NOP, if LW -> NOP*2
    instructions = []
    labels = {}
    add = 0
    for line in lines:
        if line[-1] == ':':
            labels[line[:-1]] = add
            continue
        ins = re.findall("^[a-z]+", line)
        if ins[0] != 'j':
            regs = re.findall(" [a-zA-Z0-9]+|\$[a-z]+[0-9]|[0-9]+|\$zero|-[0-9]+", line)
        else:
            regs = [line.split(" ")[1]]
        if ins[0] == 'beq' and check_dependency(instructions[-1], regs):
            if instructions[-1][0] == 'lw':
                instructions.append(['nop'])
                instructions.append(['nop'])
                add += 2
            elif r_format.get(instructions[-1][0]):
                instructions.append(['nop'])
                add += 1
            elif instructions[-1][0] in list(i_format.keys())[2:9] and i_format.get(instructions[-1][0]):
                instructions.append(['nop'])
                add += 1
        add += 1
        instructions.append(ins + regs)

    binary = []

    for add, ins in enumerate(instructions):
        b = []
        if ins[0] == 'nop':
            b.append('0' * 32)
        elif ins[0] in i_format:
            b.append(i_format[ins[0]])
            im, reg = (ins[2], ins[3]) if ins[0] in ['lw', 'sw'] else (ins[3], ins[2])
            im = im.strip()
            b.append(registers[reg])
            b.append(registers[ins[1]])
            if im.isnumeric() or (im[0] == '-' and im[1:].isnumeric()):
                immediate = int(im)
                while ins[0] == "beq" and instructions[immediate][0] == "nop":
                    immediate += 1
                if immediate < 0:
                    b.append(twos_comp(bin(immediate)[2:].zfill(16)))
                else:
                    b.append(bin(immediate)[2:].zfill(16))
            else:
                r_ad = labels[im.strip()] - add - 1
                while instructions[add + 1 + r_ad][0] == "nop":
                    r_ad += 1
                if r_ad < 0:
                    r_ad_bin = twos_comp(bin(r_ad)[2:].zfill(16))
                else:
                    r_ad_bin = bin(r_ad)[2:].zfill(16)
                b.append(r_ad_bin)

        elif ins[0] in r_format:
            b.append("000000")  # OPCODE
            if ins[0] == "sll" or ins[0] == "srl":
                b.append(registers[ins[2]])  # RT
                b.append("00000")  # RS
                b.append(registers[ins[1]])  # RD
                shamt = bin(int(ins[3]))[2:].zfill(5)
                b.append(shamt)  # SHAMT
            else:
                b.append(registers[ins[2]])  # RS
                b.append(registers[ins[3]])  # RT
                b.append(registers[ins[1]])  # RD
                b.append("00000")  # SHAMT
            b.append(r_format[ins[0]])  # FUNCT
        elif ins[0] in j_format:
            b.append(j_format[ins[0]])
            if ins[1].isnumeric():
                ad = int(ins[1])
                while instructions[ad][0] == "nop":
                    ad += 1
                b.append(bin(ad)[2:].zfill(26))
            else:
                ad = labels[ins[1]]
                while instructions[ad][0] == "nop":
                    ad += 1
                b.append(bin(ad)[2:].zfill(26))
        binary.append("".join(b))

    return binary


def compiler(file_name):
    registers = reg_init()

    lines = open(file_name).read().split('\n')

    return compile_asm(lines, registers)


# compiler("p.art")
