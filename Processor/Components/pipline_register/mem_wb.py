from Components.register_file.register import Register


class MEM_WB(Register):

    def __init__(self, clock, inputs, name="MEM_WB_Register"):
        super().__init__(clock, inputs, 71, name)
        self.wb_control: list = []
        self.memory_data = None
        self.alu_result = None
        self.rd = None
        self.build()

    def logic(self, depend=None):
        if depend is None:
            depend = []
        if self in depend:
            if Register.DEBUGMODE:
                print(self)
            return self.outputs
        depend.append(self)
        for flip_flop in self.outputs:
            flip_flop.logic(depend)
        outputs = self.get_output()
        self.rd = outputs[0:5]
        self.alu_result = outputs[5:37]
        self.memory_data = outputs[37:69]
        self.wb_control = outputs[69:71]
        return outputs

    def get_rd(self):
        return self.rd

    def get_alu_result(self):
        return self.alu_result

    def get_data_memory(self):
        return self.memory_data

    def get_wb_control(self):
        return self.wb_control
