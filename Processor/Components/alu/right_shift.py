import math

from gate.zero_gate import Zero
from multiplexer.mux_mxn import Mux_mxn


class RightSift:
    def __init__(self, a, b, width, name="RightShift"):
        self.a = a
        self.b = b
        self.width = width
        self.name = name
        self.output = None
        self.build()

    def build(self):
        size = int(math.log(self.width, 2))
        self.output = []
        zero_gate = Zero()
        for i in range(self.width):
            inputs = []
            for j in range(self.width):
                if i - j >= 0:
                    inputs.append(self.a[i - j])
                else:
                    inputs.append(zero_gate)

            self.output.append(Mux_mxn(inputs, self.b, size))
        return self.output

    def logic(self, depend=[]):
        if self in depend:
            return self.output
        for i in range(self.width):
            self.output[i].logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return [self.output[i].get_output() for i in range(self.width)]
