from Components.alu_unit import ALUUnit


class ALU:
    DEBUGMODE = True

    def __init__(self, a, b, cin, selectors, name="Arithmetic"):
        self.a = a
        self.b = b
        self.cin = cin
        self.selectors = selectors
        self.name = name
        self.outputs = None
        self.n = 32
        self.build()

    def build(self):
        self.outputs = [ALUUnit(self.a[i], self.b[i], None, self.selectors, f"{self.name}_AluUnit_{i}") for i in
                        range(self.n)]
        self.outputs[self.n - 1].set_cin(self.cin)
        for i in range(self.n - 2, -1, -1):
            self.outputs[i].set_cin(self.outputs[i + 1].cout)

    def logic(self, depend=[]):
        if self in depend:
            return self.outputs
        for unit in self.outputs:
            unit.logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return [unit.get_output()[0] for unit in self.outputs]
