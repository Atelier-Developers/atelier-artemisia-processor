from math import log

from Components.fast_memory_hierarchy.memory_cell import MemoryCell


class MemoryBank:

    def __init__(self, clock, inputs, read_address, write_address, mem_write, mem_read, size, name="FastMemoryBank"):
        self.size = size
        self.name = name
        self.inputs = inputs
        self.clock = clock
        self.write_address = write_address
        self.read_address = read_address
        self.mem_write = mem_write
        self.mem_read = mem_read
        self.output = None
        self.build()

    def build(self):
        self.output = [
            MemoryCell(self.clock, self.inputs, self.mem_write, f"{self.name}_{i}_memory_cell")
            for i in
            range(self.size)]

    def logic(self, depend=None):
        if depend is None:
            depend = []
        if self in depend:
            return self.output
        depend.append(self)
        write_add = self.write_address[-int(log(self.size, 2)) - 2:-2]
        for add in write_add:
            add.logic(depend)
        self.read_address.logic(depend)
        self.mem_read.logic(depend)
        for cell in self.output:
            cell.logic(depend)

        dec_read_address = int(self.read_address[-int(log(self.size, 2)):], 2)
        return self.output[dec_read_address].get_output() if self.mem_read else [0 for _ in range(32)]
