from math import log

from Components.memory_hierarchy.memory_cell import MemoryCell
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
        self.output = None
        self.build()

    def build(self):
        dec = Decoder_nxm(self.write_address, int(log(self.size, 2)))
        mem_cells = [
            MemoryCell(And((self.clock, dec.outputs[i], self.mem_write)), self.inputs, f"{self.name}_{i}_memory_cell")
            for i in
            range(self.size)]
        muxs = [
            Mux_mxn([mem_cells[j].output[i] for j in range(self.size)], self.read_address, int(log(self.size, 2)),
                    f"{self.name}_mux_{i}_read")
            for i in range(8)]
        self.output = [And(self.mem_read, muxs[i].output) for i in range(8)]

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
