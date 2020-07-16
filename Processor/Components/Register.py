from flipflop.d import D_FlipFlop


class Register:

    DEBUGMODE = True

    def __init__(self, clock, inputs, size, name="Register"):
        self.inputs = inputs
        self.name = name
        self.size = size
        self.clock = clock
        self.outputs = None
        self.build()

    def build(self):
        if self.inputs is None:
            return
        self.outputs = [D_FlipFlop(self.clock, self.inputs[i], f"{self.name}_FlipFlop_{i}") for i in range(self.size)]

    def set_input(self, inputs):
        self.inputs = inputs
        self.build()

    def __repr__(self):
        return f"{self.name} : {[bit.q() for bit in self.outputs]}"

    def logic(self, depend=[]):
        if self in depend:
            if Register.DEBUGMODE:
                print(self)
            return self.outputs
        for flipflop in self.outputs:
            flipflop.logic(depend + [self])
        output_bits = [bit.q() for bit in self.outputs]
        return output_bits

