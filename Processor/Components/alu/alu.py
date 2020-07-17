from Components.alu.alu_unit import ALUUnit
from Components.alu.left_shift import LeftSift
from Components.alu.right_shift import RightSift
from multiplexer.mux_mxn import Mux_mxn


class ALU:
    DEBUGMODE = True

    def __init__(self, a, b, cin, selectors, shamt, name="Arithmetic"):
        self.a = a
        self.b = b
        self.cin = cin
        # Four bits are used to select an operation, bit[0] is for alu_unit/shifting,
        # bit[1] is for shl/shr, and bit[2:4] are for the alu operation (Add, And, Or, Xor, respectively)
        self.selectors = selectors
        self.shamt = shamt
        self.name = name
        self.alu_unit_output = None
        self.output = None
        self.n = 32
        self.build()

    def build(self):
        self.alu_unit_output = [ALUUnit(self.a[i], self.b[i], None, self.selectors[2:4], f"{self.name}_AluUnit_{i}") for
                                i in
                                range(self.n)]
        self.alu_unit_output[self.n - 1].set_cin(self.cin)
        for i in range(self.n - 2, -1, -1):
            self.alu_unit_output[i].set_cin(self.alu_unit_output[i + 1].cout)

        shift_left = LeftSift(self.a, self.shamt, 32, f"{self.name}_left_shift")
        shift_right = RightSift(self.a, self.shamt, 32, f"{self.name}_right_shift")
        shift_mux = [Mux_mxn([shift_left.output[i], shift_right.output[i]], self.selectors[1:2], 1) for i in range(32)]
        self.output = [Mux_mxn([self.alu_unit_output[i].output.output, shift_mux[i].output], self.selectors[0:1], 1) for
                       i in range(32)]

    def logic(self, depend=[]):
        if self in depend:
            return self.output
        for i in range(32):
            self.output[i].logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return [unit.get_output() for unit in self.output]
