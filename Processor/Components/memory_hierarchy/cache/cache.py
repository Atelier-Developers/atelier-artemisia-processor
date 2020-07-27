from math import log

from Components.memory_hierarchy.cache.cache_set import CacheSet
from Components.memory_hierarchy.main_memory.main_memory import MainMemory
from comparator.comparator import Comparator
from decoder.decoder_mxn import Decoder_nxm
from gate.and_gate import And
from gate.zero_gate import Zero
from multiplexer.mux_mxn import Mux_mxn


class Cache:

    def __init__(self, clock, read_address, write_address, write_value, mem_write, mem_read, size, name="Cache"):
        self.clock = clock
        self.read_address = read_address
        self.write_address = write_address
        self.write_value = write_value
        self.mem_write = mem_write
        self.mem_read = mem_read
        self.size = size
        self.name = name
        self.main_memory = None
        self.sets = None
        self.output = None
        self.build()

    def build(self):
        zero = Zero()
        self.sets = [CacheSet([self.clock, self.clock], self.write_value) for i in range(self.size)]

        choice_decoder = Decoder_nxm(self.write_address[-int(log(self.size, 2)) - 2:-2],
                                     int(log(self.size, 2)))  # Chosen set

        hits = [[And((Comparator(self.write_address[0:-int(log(self.size, 2)) - 2],
                                 self.sets[i].blocks[j].tag), self.sets[i].blocks[j].valid_bit)) for
                 j in range(2)] for i in range(self.size)]

        set_clocks = [[And((self.clock, hits[i][j], choice_decoder.outputs[i], self.mem_write)) for j in range(2)] for i
                      in range(self.size)]

        for i, set in enumerate(self.sets):
            set.set_clock(set_clocks[i])

        # Write

        self.main_memory = MainMemory(self.clock, self.read_address,
                                      self.write_address, self.write_value, self.mem_write, self.mem_read, 16,
                                      f"{self.name}_Main_Memory")

        # Read

        main_memory_output = []
        for i in range(4):
            main_memory_output += self.main_memory.output[i].output



        read_muxes = [Mux_mxn((main_memory_output[i], )) for i in range(32)]
