from flipflop.d import D_FlipFlop
from latch.d import D_Latch


class Register:
    DEBUGMODE = False

    def __init__(self, clock, inputs, size, name="Register"):
        self.inputs = inputs
        self.name = name
        self.size = size
        self.clock = clock
        self.outputs = None
        self.build()

    def build(self):
        self.outputs = []
        output_app = self.outputs.append
        for i in range(self.size):
            output_app(D_FlipFlop(self.clock, None, f"{self.name}_Latch_{i}"))
        if self.inputs:
            for i in range(self.size):
                self.outputs[i].set_input(self.inputs[i])
        for i in range(self.size):
            self.outputs[i].reset()

    def set_input(self, inputs):
        self.inputs = inputs
        for i in range(self.size):
            self.outputs[i].set_input(self.inputs[i])

    def set_clock(self, clock):
        self.clock = clock
        for i in range(self.size):
            self.outputs[i].set_clock(self.clock)

    def __repr__(self):
        return f"{self.name} : {[bit.q() for bit in self.outputs]}"

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
        return self.get_output()

    def get_output(self):
        return [bit.q() for bit in self.outputs]

    def __getitem__(self, item):
        return self.outputs[item]
