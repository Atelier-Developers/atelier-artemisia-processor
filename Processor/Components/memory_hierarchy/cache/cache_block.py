from flipflop.d import D_FlipFlop
from multiplexer.mux_mxn import Mux_mxn


class CacheBlock:

    def __init__(self, clock, inputs, name="Cache_Block"):
        self.clock = clock
        self.inputs = inputs  # First bit is valid bit, second is tag, third is data
        self.name = name
        self.valid_bit = None
        self.tag = None
        self.data = None
        self.output = None
        self.build()

    def build(self):
        self.output = [D_FlipFlop(self.clock, self.inputs[i], f"{self.name}_{i}_dflipflop") for i in range(60)]
        self.valid_bit = self.output[0]
        self.tag = self.output[1:28]
        self.data = self.output[28:60]

    def logic(self, depend=None):
        if depend is None:
            depend = []
        if self in depend:
            return self.output
        depend.append(self)
        for flip in self.output:
            flip.logic(depend)
        return self.get_output()


    def set_clock(self, clock):
        self.clock = clock
        for flip in self.output:
            flip.set_clock(self.clock)

    def get_output(self):
        return [bit.q() for bit in self.output]

    def __repr__(self):
        return f"{self.name} : {self.get_output()}"
