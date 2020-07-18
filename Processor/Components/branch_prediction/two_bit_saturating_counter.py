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
        self.d1 = None
        self.build()

    def build(self):
        d1 = D_FlipFlop(self.clock, None, f"{self.name}_d_flipflop_1")
        d0 = D_FlipFlop(self.clock, None, f"{self.name}_d_flipflop_0")
        logic_d1 = Or((
            And((d0, self.input)),
            And((d1, self.input)),
            And((d0, d1))
        ))
        not_d0 = Not(d0)
        logic_d0 = Or((
            And((not_d0, self.input)),
            And((d1, not_d0)),
            And((self.input, d1))
        ))
        d1.set_input(logic_d1)
        d0.set_input(logic_d0)
        d1.reset()
        d0.reset()
        self.d0 = d0
        self.d1 = d1
        self.output = d1.output

    def logic(self, depend=[]):
        if self in depend:
            return self.output
        self.output.logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return self.output.output
