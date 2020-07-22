from Components.register_file.register import Register
from flipflop.d import D_FlipFlop


class ID_EX(Register):

    def __init__(self, clock, inputs, name="ID_EX_Register"):
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

    def build(self):
        super().build()
        out = self.outputs
        self.rd = out[0:5]
        self.rt = out[5:10]
        self.rs = out[10:15]
        self.immediate = out[15:47]
        self.funct = self.immediate[26:32]
        self.read_val2 = out[47:79]
        self.read_val1 = out[79:111]
        self.ex_control = out[111:115]  # Indexes 0, 1 , and [2,3] are respectively RegDst, AluSrc, and AluOP
        self.mem_control = out[115:117]  # Indexes 0, and 1 are respectively MemRead, and MemWrite
        self.wb_control = out[117:119]  # Indexes 0 and 1 are respectively MemToReg, and RegWrite

    # TODO change get to bit evaluation
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
