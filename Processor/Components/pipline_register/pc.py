from Components.register_file.register import Register


class PC(Register):

    def __init__(self, clock, inputs, name="PC_Register"):
        super().__init__(clock, inputs, 32, name)  # The clock should be the AND of the clock and PC.Write
        self.instruction_address = None
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
        self.instruction_address = outputs
        return outputs
