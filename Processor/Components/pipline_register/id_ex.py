from Components.register_file.register import Register
from flipflop.d import D_FlipFlop


class ID_EX(Register):

    def __init__(self, clock, inputs, name="IF_ID_Register"):
        super().__init__(clock, inputs, 119, name)
        self.wb_control: list = []
        self.mem_control: list = []
        self.ex_control: list = []
        self.rs = None
        self.rt = None
        self.rd = None
        self.read_val1 = None
        self.read_val2 = None
        self.immediate = None
        self.funct = None
        self.build()

    def logic(self, depend=None):
        if depend is None:
            depend = []
        if self in depend:
            return self.outputs
        depend.append(self)
        for flip_flop in self.outputs:
            flip_flop.logic(depend)
        outputs = self.get_output()
        self.rd = outputs[0:5]
        self.rt = outputs[5:10]
        self.rs = outputs[10:15]
        self.immediate = outputs[15:47]
        self.funct = self.immediate[26:32]
        self.read_val2 = outputs[47:79]
        self.read_val1 = outputs[79:111]
        self.ex_control = outputs[111:115]  # Indexes 0, 1 , and [2,3] are respectively RegDst, AluSrc, and AluOP
        self.mem_control = outputs[115:117]  # Indexes 0, and 1 are respectively MemRead, and MemWrite
        self.wb_control = outputs[117:119]  # Indexes 0 and 1 are respectively MemToReg, and RegWrite
        return outputs

    def get_rs(self):
        return self.rs

    def get_rt(self):
        return self.rt

    def get_rd(self):
        return self.rd

    def get_read_val1(self):
        return self.read_val1

    def get_read_val2(self):
        return self.read_val2

    def get_immediate(self):
        return self.immediate

    def get_wb_control(self):
        return self.wb_control

    def get_ex_control(self):
        return self.ex_control

    def get_mem_control(self):
        return self.mem_control

    def get_funct(self):
        return self.funct
