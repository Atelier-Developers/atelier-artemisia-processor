from Components.memory_hierarchy.cache.cache_block import CacheBlock


class CacheSet:

    def __init__(self, clock, inputs, name="Cache_Set"):
        self.clock = clock  # Maybe two clocks?
        self.inputs = inputs
        self.name = name
        self.output = None
        self.blocks = None
        self.build()

    def build(self):
        self.blocks = [CacheBlock(self.clock[i], self.inputs) for i in range(2)]
        self.output = self.blocks

    def logic(self, depend=None):
        if depend is None:
            depend = []
        if self in depend:
            return self.output
        depend.append(self)
        for block in self.output:
            block.logic(depend)
        return self.output

    def set_clock(self, clocks):
        self.clock = clocks
        for i, block in enumerate(self.blocks):
            block.set_clock(self.clock[i])

    def set_input(self, inputs):
        self.inputs = inputs

    def get_output(self):
        return [block.get_output() for block in self.output]

    def __repr__(self):
        return f"{self.name} : {self.output}"