from Components.forwading_unit.forwarding_unit import ForwardingUnit
from comparator.comparator import Comparator
from gate.and_gate import And
from gate.not_gate import Not
from gate.zero_gate import Zero


class BranchForwardingUnit(ForwardingUnit):

    def __init__(self, branch, rd_ex_mem, rd_mem_wb, rw_ex_mem, rw_mem_wb, rs_if_id, rt_if_id,
                 name="BranchForwardingUnit"):
        self.rd_ex_mem = rd_ex_mem
        self.rw_ex_mem = rw_ex_mem
        self.rs_if_id = rs_if_id
        self.rt_if_id = rt_if_id
        self.rd_mem_wb = rd_mem_wb
        self.rw_mem_wb = rw_mem_wb
        self.branch = branch
        self.name = name
        super(BranchForwardingUnit, self).__init__(rd_ex_mem, rd_mem_wb, rw_ex_mem, rw_mem_wb, rs_if_id, rt_if_id)
        self.build()

    def build(self):
        super().build()
        self.outputs = [[And((self.outputs[i][j], self.branch)) for j in range(2)] for i in range(2)]
