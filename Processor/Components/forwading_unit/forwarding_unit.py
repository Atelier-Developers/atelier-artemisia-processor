from comparator.comparator import Comparator
from gate.and_gate import And
from gate.not_gate import Not
from gate.zero_gate import Zero


class ForwardingUnit:
    def __init__(self, rd_ex_mem, rd_mem_wb, rw_ex_mem, rw_mem_wb, rs_id_ex, rt_id_ex, name="ForwardingUnit"):
        self.rd_ex_mem = rd_ex_mem
        self.rd_mem_wb = rd_mem_wb
        self.rw_ex_mem = rw_ex_mem
        self.rw_mem_wb = rw_mem_wb
        self.rs_id_ex = rs_id_ex
        self.rt_id_ex = rt_id_ex
        self.name = name
        self.outputs = []

        self.build()

    def build(self):
        comp_rd_ex_mem_zero = Comparator((self.rd_ex_mem, [Zero(), Zero(), Zero(), Zero(), Zero()]), 5,
                                         f"{self.name}_comp_rd_ex_mem_zero")
        comp_rd_mem_wb_zero = Comparator((self.rd_mem_wb, [Zero(), Zero(), Zero(), Zero(), Zero()]), 5,
                                         f"{self.name}_comp_rd_mem_wb_zero")

        forward_a_10 = And(
            (
                self.rw_ex_mem,
                Not(comp_rd_ex_mem_zero),
                Comparator((self.rd_ex_mem, self.rs_id_ex), 5)
            )
        )
        forward_b_10 = And(
            (
                self.rw_ex_mem,
                Not(comp_rd_ex_mem_zero),
                Comparator((self.rd_ex_mem, self.rt_id_ex), 5)
            )
        )

        forward_a_01 = And(
            (
                self.rw_mem_wb,
                Not(comp_rd_mem_wb_zero),
                Not(forward_a_10),
                Comparator((self.rd_mem_wb, self.rs_id_ex), 5)
            )
        )
        forward_b_01 = And(
            (
                self.rw_mem_wb,
                Not(comp_rd_mem_wb_zero),
                Not(forward_b_10),
                Comparator((self.rd_mem_wb, self.rt_id_ex), 5)
            )
        )

        self.outputs = (
            (forward_a_10, forward_a_01),
            (forward_b_10, forward_b_01)
        )

    def logic(self, depend=[]):
        if self in depend:
            return self.outputs
        for i in range(2):
            for j in range(2):
                self.outputs[i][j].logic()

    def get_output(self):
        return (self.outputs[0][0].output, self.outputs[0][1].output), (
            self.outputs[1][0].output, self.outputs[1][1].output)
