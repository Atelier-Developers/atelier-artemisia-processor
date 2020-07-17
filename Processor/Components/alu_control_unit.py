from gate.and_gate import And
from gate.not_gate import Not
from gate.or_gate import Or


class ALUControlUnit:
    def __init__(self, aluOp, funct, name="alu_control_unit"):
        self.aluOp = aluOp
        self.funct = funct
        self.output = None
        self.build()

    def build(self):
        not_aluop1 = Not(self.aluOp[1])
        not_aluop0 = Not(self.aluOp[0])
        not_funct4 = Not(self.funct[4])
        not_funct3 = Not(self.funct[3])
        not_funct2 = Not(self.funct[2])
        not_funct1 = Not(self.funct[1])
        not_funct0 = Not(self.funct[0])
        select_3 = And((self.aluOp[1], not_aluop0, self.funct[5], not_funct4, self.funct[3], not_funct2, not_funct1))
        select_2 = And(
            (self.aluOp[1], not_aluop0, self.funct[5], not_funct4, self.funct[3], not_funct2, not_funct1, not_funct0))
        and_0 = And(
            (self.aluOp[1], not_aluop0, self.funct[5], not_funct4, not_funct3, self.funct[2]))
        select_1 = Or(
            (And((and_0, not_funct1, self.funct[0])),
             And((and_0, self.funct[1], not_funct0))
             )
        )
        select_0 = And(
            (and_0, not_funct0)
        )
        and_cin_0 = And(
            (self.aluOp[1], not_aluop0, self.funct[5], not_funct4, not_funct3, not_funct2, self.funct[1], not_funct0)
        )
        and_cin_1 = And(
            (self.aluOp[1], not_aluop0, self.funct[5], not_funct4, self.funct[3], not_funct2, self.funct[1], not_funct0)
        )
        and_cin_2 = And(
            (not_aluop1, self.aluOp[0])
        )
        cin = Or((and_cin_0, and_cin_1, and_cin_2))
        self.output = cin, select_0, select_1, select_2, select_3

    def logic(self, depend=[]):
        if self in depend:
            return self.output
        for block in self.output:
            block.logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return [self.output[i].output for i in range(5)]
