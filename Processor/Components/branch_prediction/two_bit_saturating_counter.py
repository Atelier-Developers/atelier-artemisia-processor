from flipflop.d import D_FlipFlop
from gate.and_gate import And
from gate.not_gate import Not
from gate.or_gate import Or


class TwoBitSaturatingCounter:
    def __init__(self, inputs, clock, name="saturating_counter"):
        self.input = inputs
        self.name = name
        self.clock = clock
        self.output = None
        self.d0 = None
        self.build()

    def build(self):
        d1 = D_FlipFlop(self.clock, None, f"{self.name}_d_flipflop_1")
        d0 = D_FlipFlop(self.clock, None, f"{self.name}_d_flipflop_0")
        logic_d1 = Or((
            And((d0.output, self.input)),
            And((d1.output, self.input)),
            And((d0.output, d1.output))
        ))
        not_d0 = Not(d0.output)
        logic_d0 = Or((
            And((not_d0, self.input)),
            And((d1.output, not_d0)),
            And((self.input, d1.output))
        ))
        d1.set_input(logic_d1)
        d0.set_input(logic_d0)
        d1.reset()
        d0.reset()
        self.d0 = d0
        self.output = logic_d1

    def logic(self, depend=[]):
        if self in depend:
            return self.output
        self.output.logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return self.output.output
