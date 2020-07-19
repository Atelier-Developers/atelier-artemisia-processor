from flipflop.d import D_FlipFlop


class MemoryCell:

    def __init__(self, clock, inputs, name="MemoryCell"):
        self.name = name
        self.clock = clock
        self.inputs = inputs
        self.output = None
        self.build()

    def build(self):
        self.output = [D_FlipFlop(self.clock, self.inputs[i], f"{self.name}_{i}_dflipflop") for i in range(8)]

    def logic(self, depend=None):
        if depend is None:
            depend = []
        if self in depend:
            return self.output
        depend.append(self)
        for flip in self.output:
            flip.logic(depend)
        return self.get_output()

    def get_output(self):
        return [bit.q() for bit in self.output]
