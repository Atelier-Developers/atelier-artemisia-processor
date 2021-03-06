from math import log

from Components.memory_hierarchy.main_memory.memory_cell import MemoryCell
from decoder.decoder_mxn import Decoder_nxm
from gate.and_gate import And
from multiplexer.mux_mxn import Mux_mxn


class MemoryBank:

    def __init__(self, clock, inputs, read_address, write_address, mem_write, mem_read, size, name="MemoryBank"):
        self.size = size
        self.name = name
        self.inputs = inputs
        self.clock = clock
        self.write_address = write_address
        self.read_address = read_address
        self.mem_write = mem_write
        self.mem_read = mem_read
        self.mem_cells = None
        self.muxs = None
        self.output = None
        self.other_output = None
        self.dec = None
        self.build()

    def build(self):
        self.dec = Decoder_nxm(self.write_address[-int(log(self.size, 2)) - 2:-2], int(log(self.size, 2)))
        self.mem_cells = [
            MemoryCell(And((self.clock, self.dec.outputs[i], self.mem_write)), self.inputs,
                       f"{self.name}_{i}_memory_cell")
            for i in
            range(self.size)]
        self.muxs = [
            Mux_mxn([self.mem_cells[j].output[i] for j in range(self.size)],
                    self.read_address, int(log(self.size, 2)),
                    f"{self.name}_mux_{i}_read",
                    True)
            for i in range(8)]
        self.output = [And((self.mem_read, self.muxs[i].output)) for i in
                       range(8)]

    def logic(self, depend=None):
        if depend is None:
            depend = []
        if self in depend:
            return self.output

        depend.append(self)
        # check for memory cell logic
        for mux in self.output:
            mux.logic(depend)
        return self.get_output()

    def get_output(self):
        # ???????
        return [block.output for block in self.output]

    def __repr__(self):
        return f"{self.name}: {self.get_output()}"

    def show_content(self, address: int):
        return self.mem_cells[address].get_output()
