class SignExtend16To32:
    def __init__(self, a, name="SignExtend16To32"):
        self.a = a
        self.name = name
        self.output = None
        self.build()

    def build(self):
        self.output = [self.a[0] for _ in range(16)] + self.a
        return self.output

    def logic(self, depend=[]):
        for i in range(32):
            self.output[i].logic(depend + [self])
        return self.get_output()

    def get_output(self):
        return [self.output[i].output for i in range(32)]
