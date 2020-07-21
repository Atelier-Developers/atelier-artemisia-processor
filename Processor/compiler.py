import re

j_format = {
    "j": "000010",
    "jr": "000011"
}
i_format = {
    'beq': "000100",
    'bne': None,
    'addi': None,
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
                registers[f"$t{i}"] = b
            else:
                registers[f"{key}{i}"] = b
            n += 1
    return registers


def compile_asm(lines, registers):
    instructions = []
    for line in lines:
        ins = re.findall("^[a-z]+", line)
        regs = re.findall("\$[a-z]+[0-9]|[0-9]+|\$zero", line)
        instructions.append(ins + regs)

    binary = []

    for ins in instructions:
        b = []
        if ins[0] in i_format:
            b.append(i_format[ins[0]])
            b.append(registers[ins[1]])
            im, reg = (ins[2], ins[3]) if ins[0] in ['lw', 'sw'] else (ins[3], ins[2])
            b.append(registers[reg])
            b.append(bin(int(im))[2:].zfill(16))
        elif ins[0] in r_format:
            b.append("000000")
            b.append(registers[ins[1]])
            b.append(registers[ins[2]])
            b.append(registers[ins[3]])
            b.append("00000")
            b.append(r_format[ins[0]])
        binary.append("".join(b))

    return binary


def compiler(file_name):
    registers = reg_init()

    lines = open(file_name).read().split('\n')

    return compile_asm(lines, registers)
