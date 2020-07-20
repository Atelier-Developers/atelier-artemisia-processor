from Components.register_file.register import Register


class EX_MEM(Register):

    def __init__(self, clock, inputs, name="EX_MEM_Register"):
        super().__init__(clock, inputs, 73, name)
        self.wb_control: list = []
        self.mem_control: list = []
        self.alu_result = None
        self.second_alu_src_value = None
        self.rd = None
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
        self.second_alu_src_value = outputs[5:37]
        self.alu_result = outputs[37:69]
        self.mem_control = outputs[69:71]  # Indexes 0, and 1 are MemRead and MemWrite respectively
        self.wb_control = outputs[71:73]  # Indexes 0, and 1 are MemToReg and WriteReg respectively
        return outputs

    def get_wb_control(self):
        return self.wb_control

    def get_mem_control(self):
        return self.mem_control

    def get_alu_result(self):
        return self.alu_result

    def get_second_alu_src_value(self):
        return self.second_alu_src_value

    def get_rd(self):
        return self.rd
