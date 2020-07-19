from Components.memory_hierarchy.memory_cell import MemoryCell


class MemoryBank:

    def __init__(self, clock, inputs, size, name="MemoryBank"):
        self.size = size
        self.name = name
        self.inputs = inputs
        self.clock = clock
        self.output = None
        self.build()

    def build(self):
        self.output = [MemoryCell(self.clock, self.inputs, f"{self.name}_{i}_memory_cell" for i in range(self.size)]


    def logic(self, depend=None):
            if depend is None:
