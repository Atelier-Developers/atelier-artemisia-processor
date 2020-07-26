class MemoryCell:
    def __init__(self, clock, inputs, mem_write, name="MemoryCell"):
        self.name = name
        self.clock = clock
        self.inputs = inputs
        self.output = None
        self.mem_write = mem_write
        self.build()

    def build(self):
        self.output = [0 for _ in range(8)]

    def logic(self, depend=None):
        if depend is None:
            depend = []
        if self in depend:
            return self.output
        depend.append(self)
        self.clock.logic(depend)
        self.inputs.logic(depend)
        self.mem_write.logic(depend)
        for inputWire in self.inputs:
            inputWire.logic(depend)

        if self.clock.output and self.mem_write:
            for idx, inputWire in enumerate(self.inputs):
                self.output[idx] = inputWire.output
        return self.get_output()

    def get_output(self):
        return self.output
