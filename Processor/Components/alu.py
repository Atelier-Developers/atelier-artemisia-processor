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

    def build(self):
        self.outputs = [ALUUnit(self.a[i], self.b[i], None, self.selectors, f"{self.name}_AluUnit_{i}") for i in
                        range(32)]
        self.outputs[0].cin = self.cin
        for i in range(1, 32):
            self.outputs[i].cin = self.outputs[i - 1].full_adder.cout

    def logic(self, depend=[]):
        if self in depend:
            return self.outputs
        for unit in self.outputs:
            unit.logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return [unit.get_output() for unit in self.outputs]
