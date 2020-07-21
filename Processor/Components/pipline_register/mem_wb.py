from Components.register_file.register import Register


class MEM_WB(Register):

    def __init__(self, clock, inputs, name="MEM_WB_Register"):
        super().__init__(clock, inputs, 71, name)
        self.wb_control: list = []
        self.memory_data = None
        self.alu_result = None
        self.rd = None
        self.build()

    def build(self):
        super().build()
        out = [self.outputs[i].output for i in range(len(self.outputs))]
        self.rd = out[0:5]
        self.alu_result = out[5:37]
        self.memory_data = out[37:69]
        self.wb_control = out[69:71]

    def get_rd(self):
        return self.rd

    def get_alu_result(self):
        return self.alu_result

    def get_data_memory(self):
        return self.memory_data

    def get_wb_control(self):
        return self.wb_control
