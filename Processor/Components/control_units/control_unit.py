from gate.and_gate import And
from gate.not_gate import Not
from gate.or_gate import Or


class ControlUnit:

    def __init__(self, opcode, name="ControlUnit"):
        self.opcode = opcode
        self.output = None
        self.name = name
        self.build()

    def build(self):
        not_opcode5 = Not(self.opcode[5])
        not_opcode4 = Not(self.opcode[4])
        not_opcode3 = Not(self.opcode[3])
        not_opcode2 = Not(self.opcode[2])
        not_opcode1 = Not(self.opcode[1])
        not_opcode0 = Not(self.opcode[0])

        and0 = And((not_opcode5, not_opcode4, not_opcode3, not_opcode2, not_opcode1, not_opcode0), f"{self.name}_and0")
        alu_op1 = and0
        alu_op0 = And((not_opcode5, not_opcode4, not_opcode3, self.opcode[2], not_opcode1, not_opcode0))
        reg_dst = and0
        alu_src = And((self.opcode[5], not_opcode4, not_opcode2, self.opcode[1], self.opcode[0]),
                      f"{self.name}_and_alusrc")
        mem_to_reg = alu_src
        and1 = And((self.opcode[5], not_opcode4, not_opcode3, not_opcode2, self.opcode[1], self.opcode[0]),
                   f"{self.name}_and1")
        reg_write = Or((and0, and1))
        mem_read = and1
        mem_write = And((self.opcode[5], not_opcode4, self.opcode[3], not_opcode2, self.opcode[1], self.opcode[0]),
                        f"{self.name}_and_memwrite")
        branch = alu_op0
        jump = And((not_opcode5, not_opcode4, not_opcode3, not_opcode2, self.opcode[1]), f"{self.name}_and_jump")
        self.output = alu_op0, alu_op1, reg_dst, alu_src, mem_to_reg, reg_write, mem_read, mem_write, branch, jump

    def logic(self, depend=[]):
        if self in depend:
            return self.output
        for block in self.output:
            block.logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return [self.output[i].output for i in range(len(self.output))]
