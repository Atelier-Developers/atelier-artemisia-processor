from adder.full_adder import FullAdder
from gate.and_gate import And
from gate.or_gate import Or
from gate.xor_gate import Xor
from multiplexer.mux4x2 import Mux4x2


class ALUUnit:
    DEBUGMODE = True

    def __init__(self, a, b, cin, selectors, name="Arithmetic"):
        self.name = name
        self.a = a
        self.b = b
        self.cin = cin
        self.output = None
        self.full_adder: FullAdder = None
        self.selectors = selectors

    def build(self):
        full_adder = FullAdder((self.a, self.b), self.cin, f"{self.name}_arithmetic")
        and1 = And((self.a, self.b), f"{self.name}_and")
        or1 = Or((self.a, self.b), f"{self.name}_or")
        xor1 = Xor((self.a, self.b), f"{self.name}_xor")
        mux1 = Mux4x2((full_adder, and1, or1, xor1), self.selectors, f"{self.name}_mux2x4")

        self.output = mux1
        self.full_adder = full_adder

    def logic(self, depend=[]):
        if self in depend:
            if ALUUnit.DEBUGMODE:
                print(self)
            return self.output
        self.output.logic(depend + [self])
        return self.output.output.output, self.full_adder.cout

    def __repr__(self):
        return f"{self.name} : {self.output}"
