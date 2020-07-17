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
        self.output = [Mux_mxn(None, self.b, 5) for _ in range(32)]
        zero_gate = Zero()
        for i in range(32):
            inputs = []
            for j in range(32):
                if i - j >= 0:
                    inputs.append(self.a[i - j])
                else:
                    inputs.append(zero_gate.output)

            self.output[i].set_input(inputs)
        return self.output

    def logic(self, depend=[]):
        if self in depend:
            return self.output
        for i in range(32):
            self.output[i].logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return [self.output[i].get_output() for i in range(32)]
