from Components.fast_memory_hierarchy.memory_bank import MemoryBank


class MainMemory:

    def __init__(self, clock, read_address, write_address, write_value, mem_write, mem_read, size,
                 name="FastMainMemory"):
        self.size = size
        self.name = name
        self.clock = clock
        self.read_address = read_address  # log(size) width
        self.write_address = write_address  # log(size) width
        self.mem_write = mem_write
        self.write_value = write_value  # 32bit width
        self.mem_read = mem_read
        self.output = None
        self.build()

    def build(self):
        self.output = [MemoryBank(self.clock, self.write_value[i * 8: (i + 1) * 8],
                                  self.read_address,
                                  self.write_address, self.mem_write, self.mem_read,
                                  self.size,
                                  f"{self.name}_mem_bank_{i}") for i in range(4)]

    def logic(self, depend=None):
        if depend is None:
            depend = []
        if self in depend:
            return self.output
        depend.append(self)
        for bank in self.output:
            bank.logic(depend)
        return self.get_output()

    def get_output(self):
        res = []
        for bank in self.output:
            res += bank.get_output()
        return res

    def __repr__(self):
        return f"{self.name}: {self.get_output()}"
